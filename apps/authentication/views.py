from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from .models import User
from .forms import UserCreationForm, UserChangeForm
from django.contrib import messages
import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import FileResponse, HttpResponse
from apps.evidence.models import Evidence, CustodyChain
from django.utils import timezone


class LoginView(auth_views.LoginView):
  """Vista personalizada para el inicio de sesión."""
  
  template_name = 'authentication/login.html'
  redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
  """Vista personalizada para el cierre de sesión."""
  
  template_name = 'authentication/logout.html'
  next_page = reverse_lazy('authentication:login')


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
  """Vista para el perfil del usuario."""
  
  template_name = 'authentication/profile.html'


# Decorador para restringir a administradores
admin_required = user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'role') and u.role == 'admin'))

@admin_required
def admin_panel(request):
    total_users = User.objects.count()
    total_evidences = Evidence.objects.count()
    total_movements = CustodyChain.objects.count()
    recent_evidences = Evidence.objects.order_by('-created_at')[:5]
    recent_movements = CustodyChain.objects.select_related('evidence', 'received_by').order_by('-date')[:5]
    return render(request, 'authentication/admin_panel.html', {
        'total_users': total_users,
        'total_evidences': total_evidences,
        'total_movements': total_movements,
        'recent_evidences': recent_evidences,
        'recent_movements': recent_movements,
    })

@method_decorator(admin_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'authentication/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

@method_decorator(admin_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    template_name = 'authentication/user_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('authentication:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuario creado exitosamente.')
        return response

@method_decorator(admin_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'authentication/user_form.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('authentication:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Usuario actualizado exitosamente.')
        return response

@method_decorator(admin_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'authentication/user_confirm_delete.html'
    success_url = reverse_lazy('authentication:user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Usuario eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

@admin_required
def export_users_csv(request):
    users = User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=usuarios.csv'
    writer = csv.writer(response)
    writer.writerow(['Usuario', 'Nombre', 'Email', 'Rol', 'Activo'])
    for u in users:
        writer.writerow([u.username, u.get_full_name(), u.email, u.get_role_display(), 'Sí' if u.is_active else 'No'])
    return response

@admin_required
def export_users_pdf(request):
    users = User.objects.all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, 750, "Listado de Usuarios")
    p.setFont("Helvetica", 10)
    y = 720
    headers = ["Usuario", "Nombre", "Email", "Rol", "Activo"]
    for i, h in enumerate(headers):
        p.drawString(30 + i*100, y, h)
    y -= 20
    for u in users:
        p.drawString(30, y, u.username)
        p.drawString(130, y, u.get_full_name())
        p.drawString(230, y, u.email)
        p.drawString(330, y, u.get_role_display())
        p.drawString(430, y, 'Sí' if u.is_active else 'No')
        y -= 18
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='usuarios.pdf') 