from django.contrib import admin
from .models import Evidence, CustodyChain

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ("code", "case_number", "type", "collector", "created_at", "is_sensitive")
    search_fields = ("code", "case_number", "description")
    list_filter = ("type", "is_sensitive", "created_at")

@admin.register(CustodyChain)
class CustodyChainAdmin(admin.ModelAdmin):
    list_display = ("evidence", "date", "received_by", "handed_by", "reason", "destination")
    search_fields = ("evidence__code", "reason", "destination")
    list_filter = ("date",) 