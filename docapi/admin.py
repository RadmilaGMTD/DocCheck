from django.contrib import admin, messages
from .models import Document
from .tasks import send_email_admin


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "file", "uploaded_at")
    list_filter = ("status",)
    actions = ["approve_documents", "reject_documents"]

    def approve_documents(self, request, queryset):
        updated = queryset.filter(status="check").update(status="accepted")
        self.message_user(request, f"Проверен документ, статус - {updated}", messages.SUCCESS)

    approve_documents.short_description = "Подтвердить выбранные документы"

    def reject_documents(self, request, queryset):
        updated = queryset.filter(status="check").update(status="rejected")
        self.message_user(request, f"Проверен документ, статус - {updated}", messages.SUCCESS)

    reject_documents.short_description = "Отклонить выбранные документы"
