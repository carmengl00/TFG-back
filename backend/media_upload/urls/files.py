from django.urls import path

from media_upload.rest_views import UploadFileView

urlpatterns = [
    path(
        "upload_file/<str:filename>/<str:token>/",
        UploadFileView.as_view(),
        name="upload_file",
    ),
]
