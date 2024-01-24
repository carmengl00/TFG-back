from django.contrib.auth.backends import ModelBackend

from base.jwt import get_token_from_request, get_user_from_access_token


class JSONWebTokenBackend(ModelBackend):
    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        token = get_token_from_request(request)
        if not token:
            return None
        return get_user_from_access_token(token)
