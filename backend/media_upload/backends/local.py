import datetime
import os

from django.conf import settings
from django.core import signing
from django.core.files.storage import default_storage
from django.core.signing import BadSignature
from rest_framework.response import Response
from rest_framework.reverse import reverse

from media_upload.backends.base import BaseMediaUploadBackend
from media_upload.models import UploadToken


class LocalMediaUploadBackend(BaseMediaUploadBackend):
    def get_presigned_url(self, private=False):
        filename = self._get_filename()
        mimetype = self._get_content_type(filename)
        context = self.request.get("context")
        user = context.user
        name = default_storage.get_available_name(self._full_path(filename, user))

        timestamp = datetime.datetime.now().timestamp()
        token = signing.dumps({"date": timestamp, "full_path": name})

        UploadToken.objects.create(token=token)
        result = reverse("upload_file", kwargs={"token": token, "filename": filename})
        return {
            "uploadUrl": context.build_absolute_uri(result),
            "contentType": mimetype,
            "retrieveUrl": context.build_absolute_uri(default_storage.url(name)),
        }

    def _full_path(self, filename, user):
        if user and user.is_authenticated:
            return os.path.join(str(user.id), filename)
        return os.path.join("anon", filename)

    def _invalid_token_response(self):
        return Response("The token is invalid or has expired", status=401)

    def process_upload(self):
        try:
            actual_date = datetime.datetime.now().timestamp()
            limit_date = actual_date - int(settings.UPLOAD_TOKEN_EXPIRE_TIME)

            token = UploadToken.objects.get(token=self.kwargs["token"])
            token_dict = signing.loads(self.kwargs["token"])
            token_date = token_dict.get("date")
            full_path = token_dict.get("full_path")

            is_valid = all([limit_date < token_date])

            if is_valid:
                uploaded_file = self.request.data["file"]
                default_storage.save(full_path, uploaded_file, max_length=100)
                token.delete()
            else:
                token.delete()
                return self._invalid_token_response()
        except (UploadToken.DoesNotExist, BadSignature):
            return self._invalid_token_response()
        return Response(None, status=200)
