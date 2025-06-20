from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import FileResponse

from .models import Evidence, CustodyChain
from .forms import EvidenceForm, CustodyChainForm
from apps.utils.decorators import operative_required, log_activity
from apps.utils.models import ActivityLog


# Clase base para vistas que requieren permisos
class OperativeRequiredMixin(LoginRequiredMixin):
    """Mixin para vistas que requieren rol operativo."""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if request.user.is_superuser or request.user.role in ['admin', 'operative']:
            return super().dispatch(request, *args, **kwargs)
            
        messages.error(request, _('No tienes permisos para acceder a esta página.'))
        return redirect('evidence:evidence_list')


class EvidenceListView(LoginRequiredMixin, ListView):
  """Vista para listar evidencias."""
  
  model = Evidence
  template_name = 'evidence/evidence_list.html'
  context_object_name = 'evidences'
  paginate_by = 10
  
  def get_queryset(self):
    queryset = super().get_queryset()
    case_number = self.request.GET.get('case_number')
    if case_number:
      queryset = queryset.filter(case_number__icontains=case_number)
    evidence_type = self.request.GET.get('type')
    if evidence_type:
      queryset = queryset.filter(type=evidence_type)
    condition = self.request.GET.get('condition')
    if condition:
      queryset = queryset.filter(condition=condition)
    storage_location = self.request.GET.get('storage_location')
    if storage_location:
      queryset = queryset.filter(storage_location__icontains=storage_location)
    collector = self.request.GET.get('collector')
    if collector:
      queryset = queryset.filter(collector__username__icontains=collector)
    date_from = self.request.GET.get('date_from')
    if date_from:
      queryset = queryset.filter(created_at__date__gte=date_from)
    date_to = self.request.GET.get('date_to')
    if date_to:
      queryset = queryset.filter(created_at__date__lte=date_to)
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['evidence_types'] = Evidence.TYPE_CHOICES
    context['condition_choices'] = Evidence.CONDITION_CHOICES
    return context


class EvidenceDetailView(LoginRequiredMixin, DetailView):
  """Vista detalle de una evidencia."""
  
  model = Evidence
  template_name = 'evidence/evidence_detail.html'
  context_object_name = 'evidence'
  
  def get(self, request, *args, **kwargs):
    self.object = self.get_object()  # Cargar el objeto antes de usarlo
    # Log de actividad
    ActivityLog.objects.create(
        user=self.request.user,
        action=ActivityLog.ACTION_VIEW,
        content_type="Evidencia",
        object_id=str(self.object.pk),
        details=f"URL: {self.request.path}",
        ip_address=self.request.META.get('REMOTE_ADDR')
    )
    return super().get(request, *args, **kwargs)
  
  def get_context_data(self, **kwargs):
    """Añadir información de cadena de custodia al contexto."""
    context = super().get_context_data(**kwargs)
    context['custody_chain'] = self.object.custody_chain.all().order_by('-date')
    context['custody_form'] = CustodyChainForm()
    return context


class EvidenceCreateView(OperativeRequiredMixin, CreateView):
  """Vista para crear una nueva evidencia."""
  
  model = Evidence
  form_class = EvidenceForm
  template_name = 'evidence/evidence_form.html'
  success_url = reverse_lazy('evidence:evidence_list')
  
  def form_valid(self, form):
    """Procesar formulario válido."""
    form.instance.collector = self.request.user
    messages.success(self.request, _('Evidencia creada correctamente.'))
    response = super().form_valid(form)  # Guarda el objeto y asigna self.object
    # Registrar log de creación de evidencia
    ActivityLog.objects.create(
        user=self.request.user,
        action=ActivityLog.ACTION_CREATE,
        content_type="Evidencia",
        object_id=str(self.object.pk),
        details=f"URL: {self.request.path}",
        ip_address=self.request.META.get('REMOTE_ADDR')
    )
    return response

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = _('Registrar Nueva Evidencia')
    context['submit_text'] = _('Registrar')
    return context


class EvidenceUpdateView(OperativeRequiredMixin, UpdateView):
  """Vista para actualizar una evidencia existente."""
  
  model = Evidence
  form_class = EvidenceForm
  template_name = 'evidence/evidence_form.html'
  
  def get_success_url(self):
    return reverse_lazy('evidence:evidence_detail', kwargs={'pk': self.object.pk})
  
  def form_valid(self, form):
    """Procesar formulario válido."""
    messages.success(self.request, _('Evidencia actualizada correctamente.'))
    # Log de actividad
    ActivityLog.objects.create(
        user=self.request.user,
        action=ActivityLog.ACTION_UPDATE,
        content_type="Evidencia",
        object_id=str(self.object.pk),
        details=f"URL: {self.request.path}",
        ip_address=self.request.META.get('REMOTE_ADDR')
    )
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = _('Actualizar Evidencia')
    context['submit_text'] = _('Guardar Cambios')
    return context


@login_required
@operative_required
@log_activity(ActivityLog.ACTION_CREATE, "Cadena de Custodia")
def custody_chain_create(request, evidence_id):
  """Vista para crear un nuevo registro en la cadena de custodia."""
  evidence = get_object_or_404(Evidence, pk=evidence_id)
  
  if request.method == 'POST':
    form = CustodyChainForm(request.POST)
    if form.is_valid():
      custody = form.save(commit=False)
      custody.evidence = evidence
      custody.handed_by = request.user
      custody.save()
      
      # Actualizar ubicación de la evidencia
      evidence.storage_location = custody.destination
      evidence.save()
      
      messages.success(request, _('Registro de cadena de custodia creado correctamente.'))
      return redirect('evidence:evidence_detail', pk=evidence_id)
  else:
    form = CustodyChainForm()
  
  return render(request, 'evidence/custody_form.html', {
    'form': form,
    'evidence': evidence
  })


@login_required
def evidence_pdf(request, pk):
    evidence = get_object_or_404(Evidence, pk=pk)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, 750, f"Ficha de Evidencia: {evidence.code}")
    p.setFont("Helvetica", 12)
    y = 720
    p.drawString(30, y, f"Caso: {evidence.case_number}")
    y -= 20
    p.drawString(30, y, f"Tipo: {evidence.get_type_display()}")
    y -= 20
    p.drawString(30, y, f"Recolector: {evidence.collector}")
    y -= 20
    p.drawString(30, y, f"Fecha: {evidence.created_at.strftime('%d/%m/%Y %H:%M')}")
    y -= 20
    p.drawString(30, y, f"Condición: {evidence.get_condition_display()}")
    y -= 20
    p.drawString(30, y, f"Ubicación: {evidence.storage_location}")
    y -= 20
    p.drawString(30, y, f"Descripción: {evidence.description[:100]}")
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(30, y, "Historial de Cadena de Custodia:")
    y -= 20
    p.setFont("Helvetica", 10)
    for chain in evidence.custody_chain.all().order_by('-date'):
        p.drawString(30, y, f"{chain.date.strftime('%d/%m/%Y %H:%M')} - {chain.received_by} - {chain.reason}")
        y -= 15
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'ficha_{evidence.code}.pdf') 