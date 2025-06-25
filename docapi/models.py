from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование категории")
    description = models.TextField(verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Document(models.Model):
    comment = models.TextField(
        verbose_name="Комментарий к документу",
        null=True,
        blank=True,
    )
    file = models.FileField(upload_to="docapi/documents/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    STATUSES_CHOICES = [("check", "На проверке"), ("accepted", "Принят"), ("rejected", "Нужно доработать")]
    status = models.CharField(max_length=20, choices=STATUSES_CHOICES, verbose_name="Статус", default="check")
    uploaded_at = models.DateTimeField(auto_now=True, verbose_name="Загрузка документа")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.status
