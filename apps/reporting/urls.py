from django.urls import path
from apps.reporting import views

app_name = 'reporting'

urlpatterns = [
  path('', views.report_list, name='report_list'),
  path('evidence-by-type/', views.evidence_by_type_report, name='evidence_by_type'),
  path('user-activity/', views.user_activity_report, name='user_activity'),
  path('export/csv/', views.export_evidences_csv, name='export_csv'),
  path('export/pdf/', views.export_evidences_pdf, name='export_pdf'),
  path('evidence-by-type/pdf/', views.evidence_by_type_pdf, name='evidence_by_type_pdf'),
  path('user-activity/pdf/', views.user_activity_pdf, name='user_activity_pdf'),
  path('custody-chain/', views.custody_chain_report, name='custody_chain'),
  path('evidence-by-period/', views.evidence_by_period_report, name='evidence_by_period'),
  path('sensitive-evidences/', views.sensitive_evidences_report, name='sensitive_evidences'),
  path('custody-chain/csv/', views.custody_chain_csv, name='custody_chain_csv'),
  path('custody-chain/pdf/', views.custody_chain_pdf, name='custody_chain_pdf'),
  path('evidence-by-period/csv/', views.evidence_by_period_csv, name='evidence_by_period_csv'),
  path('evidence-by-period/pdf/', views.evidence_by_period_pdf, name='evidence_by_period_pdf'),
  path('sensitive-evidences/csv/', views.sensitive_evidences_csv, name='sensitive_evidences_csv'),
  path('sensitive-evidences/pdf/', views.sensitive_evidences_pdf, name='sensitive_evidences_pdf'),
] 