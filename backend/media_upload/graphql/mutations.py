import strawberry
from django.conf import settings
from django.utils.module_loading import import_string
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from media_upload.graphql.inputs import GetUploadUrlInput
from media_upload.graphql.types import MediaUploadUrlType


@strawberry.type
class Mutation:
    @login_required
    @strawberry.mutation
    def get_upload_url(
        self, info: Info, input: GetUploadUrlInput
    ) -> MediaUploadUrlType:
        config = {
            "content_type": input.content_type,
            "filename": input.filename,
            "context": info.context.request,
        }
        backend = import_string(settings.MEDIA_UPLOAD_BACKEND)
        file = backend(config).get_presigned_url(private=input.private)
        if file is None:
            raise Exception("Invalid data!")

        return MediaUploadUrlType(
            upload_url=file.get("uploadUrl"),
            content_type=file.get("contentType"),
            retrieve_url=file.get("retrieveUrl"),
        )
