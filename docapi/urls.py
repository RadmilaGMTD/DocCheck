from django.urls import path

from docapi.apps import DocapiConfig

from .views import DocumentListApiView

app_name = DocapiConfig.name


urlpatterns = [
    path("list/", DocumentListApiView.as_view(), name="docapi_list"),
]
