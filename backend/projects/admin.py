from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "tags", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("status", "is_published")
    search_fields = ("title", "description")

    fieldsets = (
        ("Негізгі", {"fields": ("title", "description", "status")}),
        ("Қосымша", {"fields": ("tags", "image", "link")}),
        ("Көрсету", {"fields": ("order", "is_published")}),
    )
