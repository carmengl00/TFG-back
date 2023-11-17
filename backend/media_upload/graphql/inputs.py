import strawberry


@strawberry.input
class GetUploadUrlInput:
    content_type: str
    filename: str
    private: bool
