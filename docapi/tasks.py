from celery import shared_task
from django.core.mail import send_mail

from config import settings
from config.settings import ADMIN_EMAIL

from .models import Document


@shared_task()
def send_email_admin(document_id):
    """
    Отправляет email администратору о получении нового документа.
    """
    doc = Document.objects.select_related("user").get(id=document_id)
    send_mail(
        subject="Получен документ",
        message=(
            f"Вам отправлен документ от пользователя {doc.user.email}\n"
            f"{'Комментарий: ' + doc.comment if doc.comment else ''}"
        ).strip(),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[ADMIN_EMAIL],
        fail_silently=False,
    )


@shared_task()
def send_email_user(document_id):
    """
    Отправляет email пользователю об изменении статуса его документа.
    """
    doc = Document.objects.select_related("user").get(id=document_id)
    if doc.status in ["accepted", "rejected"]:
        send_mail(
            subject="Статус изменен",
            message=(
                f"Ваш документ рассмотрен, статус - {doc.status}\n"
                f"{'Комментарий: ' + doc.comment if doc.comment else ''}"
            ).strip(),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[doc.user.email],
            fail_silently=False,
        )
