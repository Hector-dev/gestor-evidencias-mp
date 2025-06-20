from django.contrib import admin
from .models import ActivityLog, Backup

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "content_type", "object_id", "ip_address", "timestamp")
    search_fields = ("user__username", "action", "content_type", "object_id", "ip_address")
    list_filter = ("action", "content_type", "timestamp")
    actions = None  # Deshabilitar acciones masivas

    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):
    list_display = ("fecha", "usuario", "tipo", "archivo")
    search_fields = ("usuario__username", "tipo")
    list_filter = ("tipo", "fecha") 