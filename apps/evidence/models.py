from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Evidence(models.Model):
  """Modelo para almacenar información de evidencias."""
  
  # Tipos de evidencia
  TYPE_CHOICES = [
    ('DOCUMENT', _('Documento')),
    ('PHOTO', _('Fotografía')),
    ('VIDEO', _('Video')),
    ('AUDIO', _('Audio')),
    ('OBJECT', _('Objeto físico')),
    ('DIGITAL', _('Evidencia digital')),
    ('SAMPLE', _('Muestra biológica')),
    ('OTHER', _('Otro')),
  ]
  
  # Condiciones de la evidencia
  CONDITION_CHOICES = [
    ('EXCELLENT', _('Excelente')),
    ('GOOD', _('Buena')),
    ('FAIR', _('Regular')),
    ('POOR', _('Mala')),
    ('DAMAGED', _('Dañada')),
  ]
  
  # Campos de la evidencia
  case_number = models.CharField(
    _('número de caso'),
    max_length=50,
    help_text=_('Número de caso al que pertenece la evidencia')
  )
  
  code = models.CharField(
    _('código de evidencia'),
    max_length=50,
    unique=True,
    help_text=_('Código único de la evidencia')
  )
  
  description = models.TextField(
    _('descripción'),
    help_text=_('Descripción detallada de la evidencia')
  )
  
  type = models.CharField(
    _('tipo'),
    max_length=20,
    choices=TYPE_CHOICES,
    default='OBJECT',
    help_text=_('Tipo de evidencia')
  )
  
  location_found = models.CharField(
    _('lugar encontrado'),
    max_length=255,
    help_text=_('Lugar donde se encontró la evidencia')
  )
  
  date_found = models.DateTimeField(
    _('fecha y hora encontrada'),
    help_text=_('Fecha y hora en que se encontró la evidencia')
  )
  
  collector = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='collected_evidences',
    verbose_name=_('recolector'),
    help_text=_('Persona que recolectó la evidencia')
  )
  
  condition = models.CharField(
    _('condición'),
    max_length=20,
    choices=CONDITION_CHOICES,
    default='GOOD',
    help_text=_('Estado de la evidencia')
  )
  
  packaging = models.CharField(
    _('embalaje'),
    max_length=255,
    help_text=_('Tipo de embalaje utilizado')
  )
  
  storage_location = models.CharField(
    _('ubicación de almacenamiento'),
    max_length=255,
    help_text=_('Ubicación actual de almacenamiento')
  )
  
  notes = models.TextField(
    _('notas'),
    blank=True,
    help_text=_('Notas adicionales sobre la evidencia')
  )
  
  photo = models.ImageField(
    _('fotografía'),
    upload_to='evidences/%Y/%m/',
    blank=True,
    null=True,
    help_text=_('Fotografía de la evidencia')
  )
  
  is_sensitive = models.BooleanField(
    _('es sensible'),
    default=False,
    help_text=_('Indicar si la evidencia es de naturaleza sensible')
  )
  
  created_at = models.DateTimeField(
    _('creado en'),
    auto_now_add=True
  )
  
  updated_at = models.DateTimeField(
    _('actualizado en'),
    auto_now=True
  )
  
  class Meta:
    verbose_name = _('evidencia')
    verbose_name_plural = _('evidencias')
    ordering = ['-created_at']
  
  def __str__(self) -> str:
    return f"{self.code} - {self.description[:50]}"
  
  def save(self, *args, **kwargs):
    # Generar código único si es nuevo
    if not self.code:
      import uuid
      case_prefix = self.case_number.replace('-', '').upper()[:5]
      unique_id = str(uuid.uuid4().hex)[:8].upper()
      self.code = f"EV-{case_prefix}-{unique_id}"
    
    super().save(*args, **kwargs)


class CustodyChain(models.Model):
  """Modelo para registrar la cadena de custodia de evidencias."""
  
  evidence = models.ForeignKey(
    Evidence,
    on_delete=models.CASCADE,
    related_name='custody_chain',
    verbose_name=_('evidencia')
  )
  
  date = models.DateTimeField(
    _('fecha y hora'),
    auto_now_add=True
  )
  
  received_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='received_evidences',
    verbose_name=_('recibido por')
  )
  
  handed_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.PROTECT,
    related_name='handed_evidences',
    verbose_name=_('entregado por'),
    null=True,
    blank=True
  )
  
  reason = models.CharField(
    _('motivo'),
    max_length=255,
    help_text=_('Motivo del cambio de custodia')
  )
  
  destination = models.CharField(
    _('destino'),
    max_length=255,
    help_text=_('Destino o ubicación después del traspaso')
  )
  
  notes = models.TextField(
    _('notas'),
    blank=True,
    help_text=_('Notas adicionales sobre el traspaso')
  )
  
  class Meta:
    verbose_name = _('cadena de custodia')
    verbose_name_plural = _('cadenas de custodia')
    ordering = ['-date']
  
  def __str__(self) -> str:
    return f"Traspaso de {self.evidence.code} a {self.received_by} ({self.date.strftime('%d/%m/%Y %H:%M')})" 