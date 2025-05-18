from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Evidence, CustodyChain


class EvidenceForm(forms.ModelForm):
  """Formulario para el registro de evidencias."""
  
  class Meta:
    model = Evidence
    fields = [
      'case_number', 
      'description', 
      'type', 
      'location_found',
      'date_found', 
      'collector', 
      'condition',
      'packaging', 
      'storage_location',
      'notes',
      'photo',
      'is_sensitive'
    ]
    widgets = {
      'date_found': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
      'description': forms.Textarea(attrs={'rows': 3}),
      'notes': forms.Textarea(attrs={'rows': 3}),
    }


class CustodyChainForm(forms.ModelForm):
  """Formulario para registrar cambios en la cadena de custodia."""
  
  class Meta:
    model = CustodyChain
    fields = [
      'evidence',
      'received_by',
      'handed_by',
      'reason',
      'destination',
      'notes',
    ]
    widgets = {
      'notes': forms.Textarea(attrs={'rows': 3}),
    } 