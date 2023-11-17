import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings

from media_upload.backends.base import BaseMediaUploadBackend


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(
            signature_version="s3v4", region_name=settings.AWS_S3_REGION_NAME
        ),
    )


def create_presigned_url(method, params, expiration, client=None):
    if client is None:
        client = get_s3_client()
    return client.generate_presigned_url(method, Params=params, ExpiresIn=expiration)


class S3MediaUploadBackend(BaseMediaUploadBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_client = get_s3_client()

    def _get_filename(self, private=False):
        filename = self.request.get("filename", "data")
        location = self._get_location(private)
        if location:
            filename = "/".join([location, filename])
        prefix, *ext = filename.rsplit(".", 1)
        bucket = self.s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=prefix
        )
        keys = [i["Key"] for i in bucket.get("Contents", [])]
        while filename in keys:
            base, *ext = filename.rsplit(".", 1)
            base = "%s_" % base
            ext.insert(0, base)
            filename = ".".join(ext)
        return filename

    def _get_location(self, private=False):
        if private:
            return getattr(settings, "PRIVATE_MEDIA_LOCATION", "")
        else:
            return getattr(settings, "PUBLIC_MEDIA_LOCATION", "")

    def get_presigned_url(self, private=False):
        filename = self._get_filename(private)
        mimetype = self._get_content_type(filename)
        params = {
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": filename,
            "ContentType": mimetype,
        }
        if private:
            params.update({"ACL": "private"})
        else:
            params.update({"ACL": "public-read"})
        try:
            response = create_presigned_url(
                method="put_object",
                params=params,
                expiration=int(
                    getattr(settings, "MEDIA_UPLOAD_TOKEN_EXPIRATION", 3600)
                ),
                client=self.s3_client,
            )
        except ClientError:
            return
        return {
            "uploadUrl": response,
            "contentType": mimetype,
            "retrieveUrl": response.split("?")[0],
        }
