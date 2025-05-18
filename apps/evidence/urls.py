from django.urls import path

from . import views

app_name = 'evidence'

urlpatterns = [
  path('', views.EvidenceListView.as_view(), name='evidence_list'),
  path('<int:pk>/', views.EvidenceDetailView.as_view(), name='evidence_detail'),
  path('create/', views.EvidenceCreateView.as_view(), name='evidence_create'),
  path('<int:pk>/update/', views.EvidenceUpdateView.as_view(), name='evidence_update'),
  path('<int:evidence_id>/custody/add/', views.add_custody_record, name='add_custody'),
] 