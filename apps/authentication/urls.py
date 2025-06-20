from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'authentication'

urlpatterns = [
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout/', views.LogoutView.as_view(), name='logout'),
  path('profile/', views.ProfileView.as_view(), name='profile'),
  
  # URLs adicionales para funcionalidad completa
  path('password_change/', auth_views.PasswordChangeView.as_view(
    template_name='authentication/password_change_form.html',
    success_url='/password_change/done/'
  ), name='password_change'),
  
  path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
    template_name='authentication/password_change_done.html'
  ), name='password_change_done'),
  
  path('password_reset/', auth_views.PasswordResetView.as_view(
    template_name='authentication/password_reset_form.html',
    email_template_name='authentication/password_reset_email.html',
    subject_template_name='authentication/password_reset_subject.txt',
    success_url='/password_reset/done/'
  ), name='password_reset'),
  
  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    template_name='authentication/password_reset_done.html'
  ), name='password_reset_done'),
  
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='authentication/password_reset_confirm.html',
    success_url='/reset/done/'
  ), name='password_reset_confirm'),
  
  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='authentication/password_reset_complete.html'
  ), name='password_reset_complete'),
  
  path('panel/', views.admin_panel, name='admin_panel'),
  path('usuarios/', views.UserListView.as_view(), name='user_list'),
  path('usuarios/crear/', views.UserCreateView.as_view(), name='user_create'),
  path('usuarios/<int:pk>/editar/', views.UserUpdateView.as_view(), name='user_edit'),
  path('usuarios/<int:pk>/eliminar/', views.UserDeleteView.as_view(), name='user_delete'),
  path('usuarios/export/csv/', views.export_users_csv, name='user_export_csv'),
  path('usuarios/export/pdf/', views.export_users_pdf, name='user_export_pdf'),
] 