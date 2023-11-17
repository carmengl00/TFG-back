from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework import permissions, views
from rest_framework.parsers import FileUploadParser


class MediaUploadBackendMixin:
    def get_backend(self, request, *args, **kwargs):
        backend_class = import_string(settings.MEDIA_UPLOAD_BACKEND)
        return backend_class(request, *args, **kwargs)


class UploadFileView(MediaUploadBackendMixin, views.APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = (FileUploadParser,)

    def put(self, request, *args, **kwargs):
        return self.get_backend(request, *args, **kwargs).process_upload()
