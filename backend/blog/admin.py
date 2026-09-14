from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_published")
    list_filter = ("is_published", "published_at")
    search_fields = ("title", "summary", "body")
    date_hierarchy = "published_at"

    fieldsets = (
        ("Негізгі", {"fields": ("title", "summary")}),
        ("Мәтін", {"fields": ("body",)}),
        ("Қосымша", {"fields": ("cover", "slug", "published_at", "is_published")}),
    )
