from django.conf import settings

from base.redirect import DeepLinkRedirect


def redirect_view(request, token):
    response = DeepLinkRedirect(f"{settings.URL_FRONT}/reset-password/{token}")

    return response
