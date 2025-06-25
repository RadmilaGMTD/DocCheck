from config import settings
from celery import shared_task
from django.core.mail import send_mail
from .models import Document


@shared_task()
def send_email_admin(document_id, type_message):
    doc = Document.objects.get(id=document_id)
    if type_message == 'rejected':
        subject = "Документ отклонён"
        message = f'{doc.user.email} отправил Вам документ'
    elif type_message == 'accepted':
        subject = "Документ принят"
        message = f'{doc.user.email} отправил Вам документ'
    else:
        subject = "Получен документ"
        message = f'{doc.user.email} отправил Вам документ'
    send_mail(
        subject,
        message,
        from_email=doc.user.email,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
    )


@shared_task()
def send_email_user(document_id):
    doc = Document.objects.get(id=document_id)
    if doc.status in ["accepted", "rejected"]:
        send_mail(
            "Статус изменен",
            f"Ваш документ рассмотрен, статус - {doc.status}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[doc.user.email],
            fail_silently=False,
        )
