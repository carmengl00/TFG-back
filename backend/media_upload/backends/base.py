import mimetypes


class BaseMediaUploadBackend:
    def get_presigned_url(self, private=False):
        # Subclasses must implement this
        raise NotImplementedError

    def process_upload(self, *args, **kwargs):
        # By default the upload is done outside our system
        raise Exception("The upload is done outside of our system!")

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def _get_filename(self):
        return self.request.get("filename", "data")

    def _get_content_type(self, filename):
        content_type = self.request.get(
            "contentType",
            mimetypes.guess_type(filename)[0] or "application/octet-stream",
        )
        return content_type
