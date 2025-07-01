from django.urls import path

from docapi.apps import DocapiConfig

from .views import (
    CategoryCreateView,
    CategoryDetailView,
    CategoryListApiView,
    DocumentCreateApiView,
    DocumentDetailView,
    DocumentListApiView,
)

app_name = DocapiConfig.name


urlpatterns = [
    path("list/", DocumentListApiView.as_view(), name="docapi_list"),
    path("create/", DocumentCreateApiView.as_view(), name="docapi_create"),
    path("detail/<int:pk>/", DocumentDetailView.as_view(), name="docapi_detail"),
    path("category_list/", CategoryListApiView.as_view(), name="category_list"),
    path("category_detail/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("category_create/", CategoryCreateView.as_view(), name="category_create"),
]
