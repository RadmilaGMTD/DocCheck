from rest_framework import serializers

from .models import Document, Category
from .validators import DocumentValidator


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        validators = [DocumentValidator()]
        fields = ["id", "file", "status", "uploaded_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
