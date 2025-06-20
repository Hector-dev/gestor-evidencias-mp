from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
import csv
import io
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse, FileResponse
from django.db.models import Count
from django.utils import timezone
from apps.evidence.models import Evidence, CustodyChain
from apps.utils.decorators import administrative_required, log_activity
from apps.utils.models import ActivityLog
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.utils.http import urlencode
from django.db.models.functions import TruncMonth

# Aquí vendrán las vistas para los reportes 

@login_required
def report_list(request):
  """Vista para mostrar la lista de reportes disponibles."""
  return render(request, 'reporting/report_list.html')

# Reporte de evidencias por tipo
@login_required
@administrative_required
@log_activity(ActivityLog.ACTION_VIEW, "Reporte")
def evidence_by_type_report(request):
    """Genera un reporte de evidencias agrupadas por tipo."""
    
    # Obtener datos para el reporte
    evidence_types = Evidence.objects.values('type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Preparar el contexto
    context = {
        'report_title': 'Evidencias por Tipo',
        'evidence_types': evidence_types,
        'total_evidence': sum(t['count'] for t in evidence_types),
        'generated_at': timezone.now()
    }
    
    return render(request, 'reporting/evidence_by_type.html', context)

# Reporte de actividad de usuarios
@login_required
@administrative_required
@log_activity(ActivityLog.ACTION_VIEW, "Reporte")
def user_activity_report(request):
    """Genera un reporte de actividad de usuarios."""
    
    # Obtener período de tiempo (últimos 30 días por defecto)
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Obtener logs de actividad
    activity_logs = ActivityLog.objects.filter(
        timestamp__gte=start_date
    ).select_related('user').order_by('-timestamp')
    
    # Agrupar actividad por usuario
    user_activity = ActivityLog.objects.filter(
        timestamp__gte=start_date
    ).values('user__username').annotate(
        count=Count('id')
    ).order_by('-count')[:10]  # Top 10 usuarios más activos
    
    # Preparar el contexto
    context = {
        'report_title': f'Actividad de Usuarios (Últimos {days} días)',
        'activity_logs': activity_logs,
        'user_activity': user_activity,
        'start_date': start_date,
        'end_date': timezone.now(),
        'days': days,
        'generated_at': timezone.now()
    }
    
    return render(request, 'reporting/user_activity.html', context)

def get_filtered_evidences(request):
    queryset = Evidence.objects.all()
    case_number = request.GET.get('case_number')
    if case_number:
        queryset = queryset.filter(case_number__icontains=case_number)
    evidence_type = request.GET.get('type')
    if evidence_type:
        queryset = queryset.filter(type=evidence_type)
    condition = request.GET.get('condition')
    if condition:
        queryset = queryset.filter(condition=condition)
    storage_location = request.GET.get('storage_location')
    if storage_location:
        queryset = queryset.filter(storage_location__icontains=storage_location)
    collector = request.GET.get('collector')
    if collector:
        queryset = queryset.filter(collector__username__icontains=collector)
    date_from = request.GET.get('date_from')
    if date_from:
        queryset = queryset.filter(created_at__date__gte=date_from)
    date_to = request.GET.get('date_to')
    if date_to:
        queryset = queryset.filter(created_at__date__lte=date_to)
    return queryset

def get_filters_summary(request):
    summary = []
    if request.GET.get('case_number'):
        summary.append(f"N° de caso: {request.GET['case_number']}")
    if request.GET.get('type'):
        summary.append(f"Tipo: {dict(Evidence.TYPE_CHOICES).get(request.GET['type'], request.GET['type'])}")
    if request.GET.get('condition'):
        summary.append(f"Condición: {dict(Evidence.CONDITION_CHOICES).get(request.GET['condition'], request.GET['condition'])}")
    if request.GET.get('storage_location'):
        summary.append(f"Ubicación: {request.GET['storage_location']}")
    if request.GET.get('collector'):
        summary.append(f"Recolector: {request.GET['collector']}")
    if request.GET.get('date_from'):
        summary.append(f"Desde: {request.GET['date_from']}")
    if request.GET.get('date_to'):
        summary.append(f"Hasta: {request.GET['date_to']}")
    return ", ".join(summary) if summary else "Todos los registros"

# Exportación CSV filtrada
def export_evidences_csv(request):
    evidences = get_filtered_evidences(request)
    filters_summary = get_filters_summary(request)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=evidencias.csv'
    writer = csv.writer(response)
    writer.writerow([f'Reporte de Evidencias ({filters_summary})'])
    writer.writerow(['Código', 'Caso', 'Tipo', 'Recolector', 'Fecha', 'Condición', 'Ubicación'])
    for ev in evidences:
        writer.writerow([
            ev.code, ev.case_number, ev.get_type_display(), str(ev.collector),
            ev.created_at.strftime('%d/%m/%Y'), ev.get_condition_display(), ev.storage_location
        ])
    return response

# Exportación PDF filtrada
def export_evidences_pdf(request):
    evidences = get_filtered_evidences(request)
    filters_summary = get_filters_summary(request)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, 550, "Reporte de Evidencias")
    p.setFont("Helvetica", 10)
    p.drawString(30, 530, f"Filtros: {filters_summary}")
    y = 510
    headers = ["Código", "Caso", "Tipo", "Recolector", "Fecha", "Condición", "Ubicación"]
    for i, h in enumerate(headers):
        p.drawString(30 + i*120, y, h)
    y -= 20
    for ev in evidences:
        p.drawString(30, y, ev.code)
        p.drawString(150, y, ev.case_number)
        p.drawString(270, y, ev.get_type_display())
        p.drawString(390, y, str(ev.collector))
        p.drawString(510, y, ev.created_at.strftime('%d/%m/%Y'))
        p.drawString(630, y, ev.get_condition_display())
        p.drawString(750, y, ev.storage_location[:20])
        y -= 18
        if y < 40:
            p.showPage()
            y = 550
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='evidencias.pdf')

# Exportar reporte de evidencias por tipo a PDF
def evidence_by_type_pdf(request):
    from apps.evidence.models import Evidence
    from django.db.models import Count
    data = Evidence.objects.values('type').annotate(total=Count('id')).order_by('-total')
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, 750, "Reporte de Evidencias por Tipo")
    p.setFont("Helvetica", 12)
    y = 720
    p.drawString(30, y, "Tipo")
    p.drawString(250, y, "Cantidad")
    y -= 20
    for row in data:
        p.drawString(30, y, dict(Evidence.TYPE_CHOICES).get(row['type'], row['type']))
        p.drawString(250, y, str(row['total']))
        y -= 18
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='evidencias_por_tipo.pdf')

# Exportar reporte de actividad de usuario a PDF
def user_activity_pdf(request):
    from apps.utils.models import ActivityLog
    logs = ActivityLog.objects.select_related('user').all()[:200]
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    p.setFont("Helvetica-Bold", 16)
    p.drawString(30, 550, "Reporte de Actividad de Usuarios")
    p.setFont("Helvetica", 10)
    y = 520
    headers = ["Usuario", "Acción", "Tipo", "Objeto", "IP", "Fecha"]
    for i, h in enumerate(headers):
        p.drawString(30 + i*120, y, h)
    y -= 20
    for log in logs:
        p.drawString(30, y, str(log.user))
        p.drawString(150, y, log.get_action_display())
        p.drawString(270, y, log.content_type)
        p.drawString(390, y, str(log.object_id))
        p.drawString(510, y, log.ip_address or "-")
        p.drawString(630, y, log.timestamp.strftime('%d/%m/%Y %H:%M'))
        y -= 18
        if y < 40:
            p.showPage()
            y = 550
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='actividad_usuarios.pdf')

def custody_chain_report(request):
    """Reporte de cadena de custodia: muestra todos los movimientos de evidencias."""
    from apps.evidence.models import CustodyChain
    chains = CustodyChain.objects.select_related('evidence', 'received_by', 'handed_by').order_by('-date')[:200]
    return render(request, 'reporting/custody_chain_report.html', {'chains': chains, 'now': timezone.now()})

def evidence_by_period_report(request):
    """Reporte de evidencias agrupadas por mes/año."""
    from apps.evidence.models import Evidence
    from django.db.models import Count
    evidences = Evidence.objects.annotate(period=TruncMonth('created_at')).values('period').annotate(total=Count('id')).order_by('-period')
    return render(request, 'reporting/evidence_by_period_report.html', {'evidences': evidences, 'now': timezone.now()})

def sensitive_evidences_report(request):
    """Reporte de evidencias marcadas como sensibles."""
    from apps.evidence.models import Evidence
    evidences = Evidence.objects.filter(is_sensitive=True).order_by('-created_at')
    return render(request, 'reporting/sensitive_evidences_report.html', {'evidences': evidences, 'now': timezone.now()})

def custody_chain_csv(request):
    from apps.evidence.models import CustodyChain
    chains = CustodyChain.objects.select_related('evidence', 'received_by', 'handed_by').order_by('-date')[:200]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=cadena_custodia.csv'
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Evidencia', 'Recibido por', 'Entregado por', 'Motivo', 'Destino', 'Notas'])
    for c in chains:
        writer.writerow([
            c.date.strftime('%d/%m/%Y %H:%M'), c.evidence.code, c.received_by, c.handed_by or '--', c.reason, c.destination, c.notes or '--'
        ])
    return response

def custody_chain_pdf(request):
    from apps.evidence.models import CustodyChain
    chains = CustodyChain.objects.select_related('evidence', 'received_by', 'handed_by').order_by('-date')[:200]
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, 750, "Reporte de Cadena de Custodia")
    p.setFont("Helvetica", 10)
    y = 730
    headers = ["Fecha", "Evidencia", "Recibido por", "Entregado por", "Motivo", "Destino", "Notas"]
    for i, h in enumerate(headers):
        p.drawString(30 + i*80, y, h)
    y -= 20
    for c in chains:
        p.drawString(30, y, c.date.strftime('%d/%m/%Y %H:%M'))
        p.drawString(110, y, c.evidence.code)
        p.drawString(190, y, str(c.received_by))
        p.drawString(270, y, str(c.handed_by or '--'))
        p.drawString(350, y, c.reason[:15])
        p.drawString(430, y, c.destination[:15])
        p.drawString(510, y, (c.notes or '--')[:15])
        y -= 15
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='cadena_custodia.pdf')

def evidence_by_period_csv(request):
    from apps.evidence.models import Evidence
    from django.db.models import Count
    evidences = Evidence.objects.annotate(period=TruncMonth('created_at')).values('period').annotate(total=Count('id')).order_by('-period')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=evidencias_por_periodo.csv'
    writer = csv.writer(response)
    writer.writerow(['Período', 'Total de Evidencias'])
    for row in evidences:
        writer.writerow([row['period'].strftime('%B %Y'), row['total']])
    return response

def evidence_by_period_pdf(request):
    from apps.evidence.models import Evidence
    from django.db.models import Count
    evidences = Evidence.objects.annotate(period=TruncMonth('created_at')).values('period').annotate(total=Count('id')).order_by('-period')
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, 750, "Reporte de Evidencias por Período")
    p.setFont("Helvetica", 10)
    y = 730
    p.drawString(30, y, "Período")
    p.drawString(200, y, "Total de Evidencias")
    y -= 20
    for row in evidences:
        p.drawString(30, y, row['period'].strftime('%B %Y'))
        p.drawString(200, y, str(row['total']))
        y -= 15
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='evidencias_por_periodo.pdf')

def sensitive_evidences_csv(request):
    from apps.evidence.models import Evidence
    evidences = Evidence.objects.filter(is_sensitive=True).order_by('-created_at')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=evidencias_sensibles.csv'
    writer = csv.writer(response)
    writer.writerow(['Código', 'Descripción', 'Tipo', 'Recolector', 'Fecha', 'Ubicación'])
    for ev in evidences:
        writer.writerow([
            ev.code, ev.description, ev.get_type_display(), str(ev.collector), ev.created_at.strftime('%d/%m/%Y %H:%M'), ev.storage_location
        ])
    return response

def sensitive_evidences_pdf(request):
    from apps.evidence.models import Evidence
    evidences = Evidence.objects.filter(is_sensitive=True).order_by('-created_at')
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(30, 750, "Reporte de Evidencias Sensibles")
    p.setFont("Helvetica", 10)
    y = 730
    headers = ["Código", "Descripción", "Tipo", "Recolector", "Fecha", "Ubicación"]
    for i, h in enumerate(headers):
        p.drawString(30 + i*80, y, h)
    y -= 20
    for ev in evidences:
        p.drawString(30, y, ev.code)
        p.drawString(110, y, ev.description[:15])
        p.drawString(190, y, ev.get_type_display())
        p.drawString(270, y, str(ev.collector))
        p.drawString(350, y, ev.created_at.strftime('%d/%m/%Y %H:%M'))
        p.drawString(430, y, ev.storage_location[:15])
        y -= 15
        if y < 40:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='evidencias_sensibles.pdf') 