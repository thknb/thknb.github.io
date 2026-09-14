from django.db import models


class Project(models.Model):
    """Портфолиодағы бір жоба. Админкадан қосылады, өзгертіледі, өшіріледі."""

    STATUS_CHOICES = [
        ("live", "Жұмыс істеп тұр"),
        ("done", "Аяқталды"),
        ("wip", "Жасалып жатыр"),
    ]

    title = models.CharField("Атауы", max_length=140)
    description = models.TextField("Сипаттама")

    status = models.CharField("Күйі", max_length=10, choices=STATUS_CHOICES, default="done")

    tags = models.CharField(
        "Технологиялар",
        max_length=240,
        blank=True,
        help_text="Үтірмен бөліп жаз. Мысалы: Python, Django, SQLite",
    )

    image = models.CharField(
        "Сурет файлы",
        max_length=160,
        blank=True,
        help_text="images/ папкасындағы файлдың аты. Мысалы: project-1.jpg",
    )

    link = models.URLField("Сілтеме", blank=True, help_text="GitHub немесе жобаның адресі")

    order = models.PositiveIntegerField("Реті", default=0, help_text="Кіші сан — жоғары тұрады")
    is_published = models.BooleanField("Сайтта көрінсін", default=True)

    class Meta:
        verbose_name = "Жоба"
        verbose_name_plural = "Жобалар"
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def as_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "status": self.get_status_display(),
            "image": f"images/{self.image}" if self.image else "images/project-placeholder.svg",
            "link": self.link,
            "tags": self.tag_list(),
        }
