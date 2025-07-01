from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from users.models import User

from .models import Category, Document
from .tasks import send_email_admin, send_email_user


class DocapiAPITests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(
            email="admin@test.com",
            is_superuser=True,
            is_staff=True,
        )
        self.user = User.objects.create(email="user@test.com")
        self.other_user = User.objects.create(email="other@test.com")
        self.category = Category.objects.create(name="Test Category", description="test description")
        self.document = Document.objects.create(user=self.user, file=SimpleUploadedFile("test.docx", b"test content"))

    def test_retrieve_document_as_owner(self):
        """Владелец может просматривать свой документ"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/detail/{self.document.pk}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("status"), self.document.status)

    def test_retrieve_document_as_admin(self):
        """Админ может просматривать любой документ"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"/detail/{self.document.pk}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("status"), self.document.status)

    def test_retrieve_document_as_other_user(self):
        """Чужой пользователь не может просматривать документ"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(f"/detail/{self.document.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_documents_as_user(self):
        """Обычный пользователь видит только свои документы"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.document.id)

    def test_list_documents_as_admin(self):
        """Админ видит все документы"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/list/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_by_status(self):
        """Фильтрация по статусу"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/list/" + "?status=check")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.document.id)

    @patch("docapi.tasks.send_email_admin.delay")
    def test_create_document(self, mock_delay):
        """Тест создания нового документа"""
        self.client.force_authenticate(user=self.user)
        test_file = SimpleUploadedFile(name="new.docx", content=b"file content")
        response = self.client.post("/create/", {"file": test_file}, format="multipart")
        new_doc = Document.objects.latest("id")
        mock_delay.assert_called_once_with(new_doc.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.count(), 2)
        self.assertEqual(new_doc.user.id, self.user.id)
        self.assertTrue(new_doc.file.name.endswith(".docx"))

    def test_list_categories_as_user(self):
        """Обычный пользователь может просматривать категории"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/category_list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_categories_unauthenticated(self):
        """Неаутентифицированный доступ запрещен"""
        response = self.client.get("/category_list/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_as_admin(self):
        """Админ может создавать категории"""
        self.client.force_authenticate(user=self.admin)
        data = {"name": "New Category", "description": "new description"}
        response = self.client.post("/category_create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_create_category_as_user(self):
        """Обычный пользователь не может создавать категории"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "New Category", "description": "new description"}
        response = self.client.post("/category_create/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_as_admin(self):
        """Админ может обновлять категории"""
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Updated Name"}
        response = self.client.patch(f"/category_detail/{self.category.pk}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Name")

    def test_delete_category_as_user(self):
        """Обычный пользователь не может удалять категории"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f"/category_detail/{self.category.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("docapi.tasks.send_mail")
    def test_send_email_admin_success(self, mock_send_mail):
        """Тест успешной отправки email администратору"""
        send_email_admin(self.document.id)
        mock_send_mail.assert_called_once_with(
            subject="Получен документ",
            message="Вам отправлен документ от пользователя user@test.com",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["raf1507@mail.ru"],
            fail_silently=False,
        )

    @patch("docapi.tasks.send_mail")
    def test_send_email_user_accepted(self, mock_send_mail):
        """Тест отправки email пользователю при принятии документа"""
        self.document.status = "accepted"
        self.document.save()
        send_email_user(self.document.id)
        mock_send_mail.assert_called_once_with(
            subject="Статус изменен",
            message="Ваш документ рассмотрен, статус - accepted",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["user@test.com"],
            fail_silently=False,
        )

    @patch("docapi.tasks.send_mail")
    def test_send_email_user_rejected(self, mock_send_mail):
        """Тест отправки email пользователю при отклонении документа"""
        self.document.status = "rejected"
        self.document.save()

        send_email_user(self.document.id)
        mock_send_mail.assert_called_once()

    @patch("docapi.tasks.send_mail")
    def test_send_email_user_no_status_change(self, mock_send_mail):
        """Тест, что email не отправляется при нерелевантном статусе"""
        self.document.status = "check"
        self.document.save()
        send_email_user(self.document.id)
        mock_send_mail.assert_not_called()
