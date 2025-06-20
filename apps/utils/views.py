from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.conf import settings
from .models import Backup
from django.contrib import messages
import os
import subprocess
from django.core.files.base import ContentFile
from django.utils import timezone
from django.core.paginator import Paginator
from apps.utils.models import ActivityLog
from django.utils.html import escape

# Decorador para restringir a administradores
admin_required = user_passes_test(lambda u: u.is_superuser or (hasattr(u, 'role') and u.role == 'admin'))

@method_decorator(admin_required, name='dispatch')
class BackupListView(ListView):
    model = Backup
    template_name = 'utils/backup_list.html'
    context_object_name = 'backups'
    paginate_by = 10

@admin_required
def create_backup(request):
    """Crea un backup de la base de datos y lo guarda en el modelo Backup."""
    if request.method == 'POST':
        # Ruta y nombre del archivo
        fecha = timezone.now().strftime('%Y%m%d_%H%M%S')
        filename = f"backup_{fecha}.sql"
        backup_path = os.path.join(settings.MEDIA_ROOT, 'backups', filename)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        # Comando para hacer el dump
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        cmd = [
            'pg_dump',
            '-h', db_host,
            '-p', str(db_port),
            '-U', db_user,
            '-F', 'c',  # formato custom
            '-b',
            '-v',
            '-f', backup_path,
            db_name
        ]
        try:
            subprocess.run(cmd, check=True, env=env)
            # Guardar en el modelo
            with open(backup_path, 'rb') as f:
                backup_file = ContentFile(f.read(), name=filename)
                backup = Backup.objects.create(
                    archivo=backup_file,
                    usuario=request.user,
                    tipo='manual',
                )
            messages.success(request, 'Backup creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el backup: {e}')
        return redirect(reverse('utils:backup_list'))
    return render(request, 'utils/backup_create.html')

@login_required
def download_backup(request, pk):
    backup = get_object_or_404(Backup, pk=pk)
    response = FileResponse(backup.archivo.open('rb'), as_attachment=True, filename=os.path.basename(backup.archivo.name))
    return response

@admin_required
def restore_backup(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']
        # Guardar archivo temporalmente
        temp_path = os.path.join(settings.MEDIA_ROOT, 'backups', f"restore_{timezone.now().strftime('%Y%m%d_%H%M%S')}.sql")
        with open(temp_path, 'wb+') as destination:
            for chunk in backup_file.chunks():
                destination.write(chunk)
        # Comando para restaurar
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        cmd = [
            'pg_restore',
            '-h', db_host,
            '-p', str(db_port),
            '-U', db_user,
            '-d', db_name,
            '-c',  # limpiar antes de restaurar
            temp_path
        ]
        try:
            subprocess.run(cmd, check=True, env=env)
            messages.success(request, 'Backup restaurado exitosamente. Es posible que debas reiniciar el contenedor.')
        except Exception as e:
            messages.error(request, f'Error al restaurar el backup: {e}')
        os.remove(temp_path)
        return redirect(reverse('utils:backup_list'))
    return render(request, 'utils/backup_restore.html')

@admin_required
def activity_log_list(request):
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')
    paginator = Paginator(logs, 50)
    page = request.GET.get('page')
    logs_page = paginator.get_page(page)
    return render(request, 'utils/activity_log_list.html', {'logs': logs_page})

@admin_required
def download_logs_txt(request):
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=logs_actividad.txt'
    response.write('Usuario\tAcción\tTipo\tObjeto\tIP\tFecha\n')
    for log in logs:
        response.write(f'{log.user}\t{log.get_action_display()}\t{log.content_type}\t{log.object_id}\t{log.ip_address or "-"}\t{log.timestamp.strftime("%d/%m/%Y %H:%M")}\n')
    return response 