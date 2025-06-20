from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ActivityLog(models.Model):
    """Modelo para registrar la actividad de los usuarios en el sistema."""
    
    # Tipos de acciones
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_VIEW = 'view'
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_EXPORT = 'export'
    
    ACTION_CHOICES = [
        (ACTION_CREATE, _('Creación')),
        (ACTION_UPDATE, _('Actualización')),
        (ACTION_DELETE, _('Eliminación')),
        (ACTION_VIEW, _('Visualización')),
        (ACTION_LOGIN, _('Inicio de sesión')),
        (ACTION_LOGOUT, _('Cierre de sesión')),
        (ACTION_EXPORT, _('Exportación')),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activity_logs',
        verbose_name=_('usuario')
    )
    
    action = models.CharField(
        _('acción'),
        max_length=20,
        choices=ACTION_CHOICES
    )
    
    content_type = models.CharField(
        _('tipo de contenido'),
        max_length=50,
        help_text=_('Tipo de objeto afectado (ej: Evidencia, Usuario, etc.)')
    )
    
    object_id = models.CharField(
        _('id de objeto'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Identificador del objeto afectado')
    )
    
    details = models.TextField(
        _('detalles'),
        blank=True,
        help_text=_('Detalles adicionales de la acción')
    )
    
    ip_address = models.GenericIPAddressField(
        _('dirección IP'),
        blank=True,
        null=True
    )
    
    timestamp = models.DateTimeField(
        _('fecha y hora'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('registro de actividad')
        verbose_name_plural = _('registros de actividad')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.user.username} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"


class Backup(models.Model):
    """Modelo para registrar los backups realizados y permitir su gestión desde la web."""
    BACKUP_TYPE_CHOICES = [
        ("manual", "Manual"),
        ("automatic", "Automático"),
    ]
    archivo = models.FileField("Archivo de backup", upload_to="backups/%Y/%m/%d/")
    fecha = models.DateTimeField("Fecha de backup", auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="usuario")
    tipo = models.CharField("Tipo de backup", max_length=20, choices=BACKUP_TYPE_CHOICES, default="manual")

    class Meta:
        verbose_name = "backup"
        verbose_name_plural = "backups"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Backup {self.fecha.strftime('%d/%m/%Y %H:%M')} ({self.tipo})" 