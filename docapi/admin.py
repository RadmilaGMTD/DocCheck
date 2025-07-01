import logging

from django.contrib import admin, messages

from .models import Document
from .tasks import send_email_user

logger = logging.getLogger(__name__)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "file", "uploaded_at")
    list_filter = ("status",)
    actions = ["approve_documents", "reject_documents"]

    def save_model(self, request, obj, form, change):
        """
        Отправка уведомления при ручном изменении статуса
        через форму редактирования документа
        """
        if change and "status" in form.changed_data:
            old_status = Document.objects.get(pk=obj.pk).status
            new_status = form.cleaned_data["status"]
            super().save_model(request, obj, form, change)
            if new_status in ["accepted", "rejected"] and old_status != new_status:
                send_email_user.delay(obj.id)
        else:
            super().save_model(request, obj, form, change)

    def approve_documents(self, request, queryset):
        """Подтверждение документов"""
        updated = queryset.filter(status="check").update(status="accepted")
        self.message_user(request, f"Проверен документ, статус - {updated}", messages.SUCCESS)

    approve_documents.short_description = "Подтвердить выбранные документы"

    def reject_documents(self, request, queryset):
        """Отклонение документов"""
        updated = queryset.filter(status="check").update(status="rejected")
        self.message_user(request, f"Проверен документ, статус - {updated}", messages.SUCCESS)

    reject_documents.short_description = "Отклонить выбранные документы"
