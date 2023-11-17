from typing import ClassVar

from django.http.response import HttpResponsePermanentRedirect


class DeepLinkRedirect(HttpResponsePermanentRedirect):
    allowed_schemes: ClassVar[list] = [
        "backend",
    ]
