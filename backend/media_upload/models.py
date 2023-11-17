from django.db import models

from base.models import SimpleModel


class UploadToken(SimpleModel):
    token = models.CharField(max_length=255, null=True)
