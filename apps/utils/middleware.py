import re
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.conf import settings
from apps.utils.models import ActivityLog


class ActivityLogMiddleware(MiddlewareMixin):
    """
    Middleware para registrar automáticamente las acciones de usuarios.
    Registra los accesos a vistas relevantes.
    """
    
    def get_client_ip(self, request):
        """Obtiene la IP del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """Procesa la vista y registra actividad relevante."""
        # Solo registrar si el usuario está autenticado
        if not request.user.is_authenticated:
            return None
            
        # Obtener la URL actual y el nombre de la vista
        try:
            url_name = resolve(request.path_info).url_name
        except:
            url_name = ""
            
        # Registrar solo ciertas acciones
        if url_name and any(pattern in url_name for pattern in ['create', 'update', 'delete', 'detail', 'export', 'login', 'logout']):
            # Determinar el tipo de acción
            action = ActivityLog.ACTION_VIEW  # Por defecto
            
            if 'create' in url_name:
                action = ActivityLog.ACTION_CREATE
            elif 'update' in url_name:
                action = ActivityLog.ACTION_UPDATE
            elif 'delete' in url_name:
                action = ActivityLog.ACTION_DELETE
            elif 'export' in url_name:
                action = ActivityLog.ACTION_EXPORT
            elif 'login' in url_name:
                action = ActivityLog.ACTION_LOGIN
            elif 'logout' in url_name:
                action = ActivityLog.ACTION_LOGOUT
                
            # Determinar el tipo de contenido
            content_type = "Desconocido"
            if 'evidence' in url_name:
                content_type = "Evidencia"
            elif 'user' in url_name or 'account' in url_name:
                content_type = "Usuario"
            elif 'report' in url_name:
                content_type = "Reporte"
                
            # Obtener el ID del objeto si está en la URL
            object_id = None
            for key, value in view_kwargs.items():
                if key in ['pk', 'id']:
                    object_id = value
                    break
                    
            # Registrar la actividad
            ActivityLog.objects.create(
                user=request.user,
                action=action,
                content_type=content_type,
                object_id=object_id,
                details=f"URL: {request.path}",
                ip_address=self.get_client_ip(request)
            )
            
        return None 