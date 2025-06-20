from django.urls import path
from . import views

app_name = 'utils'

urlpatterns = [
    path('backups/', views.BackupListView.as_view(), name='backup_list'),
    path('backups/create/', views.create_backup, name='backup_create'),
    path('backups/download/<int:pk>/', views.download_backup, name='backup_download'),
    path('backups/restore/', views.restore_backup, name='backup_restore'),
    path('logs/', views.activity_log_list, name='activity_log_list'),
    path('logs/download/', views.download_logs_txt, name='download_logs_txt'),
] 