from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
  """User model that extends Django's AbstractUser."""
  
  # Definición de roles
  ROLE_ADMIN = 'admin'
  ROLE_OPERATIVE = 'operative'
  ROLE_ADMINISTRATIVE = 'administrative'
  
  ROLE_CHOICES = [
    (ROLE_ADMIN, _('Administrador')),
    (ROLE_OPERATIVE, _('Operativo')),
    (ROLE_ADMINISTRATIVE, _('Administrativo')),
  ]
  
  # Campos adicionales
  identification = models.CharField(
    _("número de identificación"),
    max_length=20,
    blank=True,
    help_text=_("Número de identificación o cédula")
  )
  position = models.CharField(
    _("cargo"),
    max_length=100,
    blank=True
  )
  department = models.CharField(
    _("departamento"),
    max_length=100,
    blank=True
  )
  phone = models.CharField(
    _("teléfono"),
    max_length=20,
    blank=True
  )
  role = models.CharField(
    _("rol"),
    max_length=20,
    choices=ROLE_CHOICES,
    default=ROLE_OPERATIVE,
    help_text=_("Rol del usuario en el sistema")
  )
  
  class Meta:
    verbose_name = _("usuario")
    verbose_name_plural = _("usuarios")
    
  def __str__(self) -> str:
    return f"{self.get_full_name()} ({self.username})"
    
  def is_admin(self) -> bool:
    """Verifica si el usuario tiene rol de administrador."""
    return self.role == self.ROLE_ADMIN or self.is_superuser
    
  def is_operative(self) -> bool:
    """Verifica si el usuario tiene rol operativo."""
    return self.role == self.ROLE_OPERATIVE
    
  def is_administrative(self) -> bool:
    """Verifica si el usuario tiene rol administrativo."""
    return self.role == self.ROLE_ADMINISTRATIVE
    
  def can_create_evidence(self) -> bool:
    """Verifica si el usuario puede crear evidencias."""
    return self.is_admin() or self.is_operative()
    
  def can_edit_evidence(self) -> bool:
    """Verifica si el usuario puede editar evidencias."""
    return self.is_admin() or self.is_operative()
    
  def can_export_reports(self) -> bool:
    """Verifica si el usuario puede exportar reportes."""
    return self.is_admin() or self.is_administrative()
    
  def can_manage_users(self) -> bool:
    """Verifica si el usuario puede gestionar usuarios."""
    return self.is_admin() 