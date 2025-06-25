from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from .models import Document, Category
from .tasks import send_email_admin
from .permissions import IsOwner, IsAdmin, IsOwnerOrAdmin
from .paginators import DocumentPaginator

from .serializers import DocumentSerializer, CategorySerializer


class DocumentListApiView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DocumentPaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("status",)
    ordering_fields = ("uploaded_at",)

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class DocumentCreateApiView(generics.CreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        document = serializer.save(user=self.request.user)
        send_email_admin.delay(document.id, 'new')


class CategoryListApiView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
