from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
  """User model that extends Django's AbstractUser."""
  
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
  
  class Meta:
    verbose_name = _("usuario")
    verbose_name_plural = _("usuarios")
    
  def __str__(self) -> str:
    return f"{self.get_full_name()} ({self.username})" 