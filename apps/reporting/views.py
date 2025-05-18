from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Aquí vendrán las vistas para los reportes 

@login_required
def report_list(request):
  """Vista para mostrar la lista de reportes disponibles."""
  return render(request, 'reporting/report_list.html') 