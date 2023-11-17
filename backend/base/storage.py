from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class BaseStorage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None):
        if name.startswith(("http://", "https://")):
            return name
        return super().url(name, parameters, expire)


class StaticStorage(BaseStorage):
    location = "static"
    default_acl = "public-read"


class PublicMediaStorage(BaseStorage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False


class PrivateMediaStorage(BaseStorage):
    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class LocalStorage(FileSystemStorage):
    def url(self, name):
        if name.startswith(("http://", "https://")):
            return name
        return super().url(name)
