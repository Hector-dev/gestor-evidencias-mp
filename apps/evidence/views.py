from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Evidence, CustodyChain
from .forms import EvidenceForm, CustodyChainForm


class EvidenceListView(LoginRequiredMixin, ListView):
  """Vista para listar evidencias."""
  
  model = Evidence
  template_name = 'evidence/evidence_list.html'
  context_object_name = 'evidences'
  paginate_by = 10
  
  def get_queryset(self):
    """Filtrar evidencias según parámetros de búsqueda."""
    queryset = super().get_queryset()
    
    # Filtrar por número de caso
    case_number = self.request.GET.get('case_number')
    if case_number:
      queryset = queryset.filter(case_number__icontains=case_number)
    
    # Filtrar por tipo
    evidence_type = self.request.GET.get('type')
    if evidence_type:
      queryset = queryset.filter(type=evidence_type)
    
    return queryset


class EvidenceDetailView(LoginRequiredMixin, DetailView):
  """Vista detalle de una evidencia."""
  
  model = Evidence
  template_name = 'evidence/evidence_detail.html'
  context_object_name = 'evidence'
  
  def get_context_data(self, **kwargs):
    """Añadir información de cadena de custodia al contexto."""
    context = super().get_context_data(**kwargs)
    context['custody_chain'] = self.object.custody_chain.all().order_by('-date')
    context['custody_form'] = CustodyChainForm(initial={'evidence': self.object})
    return context


class EvidenceCreateView(LoginRequiredMixin, CreateView):
  """Vista para crear una nueva evidencia."""
  
  model = Evidence
  form_class = EvidenceForm
  template_name = 'evidence/evidence_form.html'
  success_url = reverse_lazy('evidence:evidence_list')
  
  def form_valid(self, form):
    """Procesar formulario válido."""
    messages.success(self.request, "Evidencia registrada exitosamente.")
    return super().form_valid(form)


class EvidenceUpdateView(LoginRequiredMixin, UpdateView):
  """Vista para actualizar una evidencia existente."""
  
  model = Evidence
  form_class = EvidenceForm
  template_name = 'evidence/evidence_form.html'
  
  def get_success_url(self):
    return reverse_lazy('evidence:evidence_detail', kwargs={'pk': self.object.pk})
  
  def form_valid(self, form):
    """Procesar formulario válido."""
    messages.success(self.request, "Evidencia actualizada exitosamente.")
    return super().form_valid(form)


@login_required
def add_custody_record(request, evidence_id):
  """Añadir un nuevo registro a la cadena de custodia."""
  evidence = get_object_or_404(Evidence, pk=evidence_id)
  
  if request.method == 'POST':
    form = CustodyChainForm(request.POST)
    if form.is_valid():
      custody = form.save(commit=False)
      custody.evidence = evidence
      custody.save()
      messages.success(request, "Registro de custodia añadido exitosamente.")
      return redirect('evidence:evidence_detail', pk=evidence_id)
  else:
    form = CustodyChainForm(initial={'evidence': evidence})
  
  return render(request, 'evidence/custody_form.html', {
    'form': form,
    'evidence': evidence
  }) 