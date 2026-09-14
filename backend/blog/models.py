from django.db import models
from django.utils import timezone

from .markdown import to_html
from .translit import slugify_kk


class Article(models.Model):
    """Блог жазбасы. Админкадан жазылады."""

    title = models.CharField("Тақырып", max_length=200)
    slug = models.SlugField(
        "Сілтеме", max_length=90, unique=True, blank=True,
        help_text="Бос қалдырсаң, тақырыптан автоматты жасалады.",
    )

    summary = models.TextField(
        "Қысқаша", max_length=400,
        help_text="Тізімде көрінетін 1–2 сөйлем.",
    )
    body = models.TextField(
        "Мәтін",
        help_text="Markdown: ## тақырып, - тізім, **қалың**, [мәтін](сілтеме), ![сурет](images/x.jpg)",
    )

    cover = models.CharField(
        "Мұқаба суреті", max_length=160, blank=True,
        help_text="images/ ішіндегі файл аты. Мысалы: post-1.jpg",
    )

    published_at = models.DateField("Жарияланған күні", default=timezone.localdate)
    is_published = models.BooleanField("Сайтта көрінсін", default=True)

    class Meta:
        verbose_name = "Жазба"
        verbose_name_plural = "Жазбалар"
        ordering = ["-published_at", "-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify_kk(self.title)
            slug, counter = base, 2
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def as_dict(self):
        return {
            "slug": self.slug,
            "title": self.title,
            "summary": self.summary,
            "cover": f"images/{self.cover}" if self.cover else "",
            "date": self.published_at.isoformat(),
            "html": to_html(self.body),
        }
