from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.shortcuts import redirect

# Configurar el esquema de API
schema_view = get_schema_view(
  openapi.Info(
    title="API Gestor de Evidencias",
    default_version='v1',
    description="API para gestión de evidencias del Ministerio Público",
    contact=openapi.Contact(email="contacto@mp.gob"),
    license=openapi.License(name="Licencia Ministerio Público"),
  ),
  public=True,
  permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
  # Redirigir /admin/ a /panel/
  path('admin/', lambda request: redirect('/panel/', permanent=True)),
  
  # Autenticación personalizada
  path('', include('apps.authentication.urls')),
  
  # Aplicaciones
  path('evidencias/', include('apps.evidence.urls')),
  path('reportes/', include('apps.reporting.urls')),
  path('utilidades/', include('apps.utils.urls')),
  
  # API docs
  path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  
  # Home
  path('', RedirectView.as_view(pattern_name='evidence:evidence_list'), name='home'),
]

# Debug toolbar
if settings.DEBUG:
  import debug_toolbar
  urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
  ]
  
  # Servir archivos estáticos y media en desarrollo
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 