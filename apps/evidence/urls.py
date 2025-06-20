from django.urls import path
from apps.evidence import views

app_name = 'evidence'

urlpatterns = [
  path('', views.EvidenceListView.as_view(), name='evidence_list'),
  path('crear/', views.EvidenceCreateView.as_view(), name='evidence_create'),
  path('<int:pk>/', views.EvidenceDetailView.as_view(), name='evidence_detail'),
  path('<int:pk>/editar/', views.EvidenceUpdateView.as_view(), name='evidence_update'),
  path('<int:evidence_id>/custodia/crear/', views.custody_chain_create, name='custody_create'),
  path('<int:pk>/pdf/', views.evidence_pdf, name='evidence_pdf'),
] 