import datetime

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from strawberry_django_jwt.shortcuts import get_token as get_token_jwt


def get_url_reset_password(user_id, token) -> str:
    now = datetime.datetime.now()
    past = now + datetime.timedelta(hours=10)

    encoded_token = jwt.encode(
        {"user_id": str(user_id), "token": str(token), "exp": past},
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    url = f"https://{settings.URL_API}/reset-password/{encoded_token}"

    return url


def get_token(user, password) -> str:
    user = authenticate(
        username=user.email,
        password=password,
    )

    if user is None:
        raise Exception("Please, enter valid credentials")

    token = get_token_jwt(user)
    return token
