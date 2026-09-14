from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "short_text", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "text")
    readonly_fields = ("name", "email", "text", "created_at")
    list_editable = ("is_read",)
    date_hierarchy = "created_at"

    @admin.display(description="Мәтін")
    def short_text(self, obj):
        return obj.text[:60] + ("…" if len(obj.text) > 60 else "")

    def has_add_permission(self, request):
        return False
