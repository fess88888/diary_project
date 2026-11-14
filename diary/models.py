from django.conf import settings
from django.db import models


class Entry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name="Автор",
    )
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Текст записи")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Запись дневника"
        verbose_name_plural = "Записи дневника"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
