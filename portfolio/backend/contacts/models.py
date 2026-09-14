from django.db import models


class Message(models.Model):
    """Сайттағы формадан келген хабарлама."""

    name = models.CharField("Аты", max_length=120)
    email = models.EmailField("Email", max_length=200, blank=True)
    text = models.TextField("Хабарлама", max_length=5000)
    created_at = models.DateTimeField("Келген уақыты", auto_now_add=True)
    is_read = models.BooleanField("Оқылды", default=False)

    class Meta:
        verbose_name = "Хабарлама"
        verbose_name_plural = "Хабарламалар"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%d.%m.%Y %H:%M}"
