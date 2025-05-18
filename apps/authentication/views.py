from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class LoginView(auth_views.LoginView):
  """Vista personalizada para el inicio de sesión."""
  
  template_name = 'authentication/login.html'
  redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
  """Vista personalizada para el cierre de sesión."""
  
  template_name = 'authentication/logout.html'
  next_page = reverse_lazy('login')


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
  """Vista para el perfil del usuario."""
  
  template_name = 'authentication/profile.html' 