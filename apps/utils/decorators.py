from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _
from apps.utils.models import ActivityLog


def role_required(allowed_roles):
    """
    Decorador para verificar si el usuario tiene uno de los roles permitidos.
    
    Args:
        allowed_roles: Lista de roles permitidos
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Verificar que el usuario esté autenticado
            if not request.user.is_authenticated:
                return redirect(reverse('authentication:login'))
            
            # Verificar si es superusuario (siempre tiene acceso)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            # Verificar el rol del usuario
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # Si no tiene el rol necesario, redirigir a página de inicio
            messages.error(request, _('No tienes permisos para acceder a esta página.'))
            return redirect(reverse('evidence:evidence_list'))
            
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Decorador para verificar si el usuario es administrador."""
    return role_required(['admin'])(view_func)


def operative_required(view_func):
    """Decorador para verificar si el usuario es operativo."""
    return role_required(['operative', 'admin'])(view_func)


def administrative_required(view_func):
    """Decorador para verificar si el usuario es administrativo."""
    return role_required(['administrative', 'admin'])(view_func)


def log_activity(action, content_type="", get_object_id=None):
    """
    Decorador para registrar actividad manualmente.
    
    Args:
        action: Tipo de acción a registrar
        content_type: Tipo de contenido
        get_object_id: Función para obtener el ID del objeto desde los argumentos
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Ejecutar la vista
            response = view_func(request, *args, **kwargs)
            
            # Registrar la actividad solo si el usuario está autenticado
            if request.user.is_authenticated:
                # Obtener el ID del objeto
                object_id = None
                if get_object_id:
                    object_id = get_object_id(request, args, kwargs)
                elif 'pk' in kwargs:
                    object_id = kwargs['pk']
                elif 'id' in kwargs:
                    object_id = kwargs['id']
                
                # Obtener la IP del cliente
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                
                # Crear el registro de actividad
                ActivityLog.objects.create(
                    user=request.user,
                    action=action,
                    content_type=content_type,
                    object_id=object_id,
                    details=f"URL: {request.path}",
                    ip_address=ip
                )
            
            return response
        return _wrapped_view
    return decorator 