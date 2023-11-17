import strawberry


@strawberry.type
class MediaUploadUrlType:
    upload_url: str
    content_type: str
    retrieve_url: str
