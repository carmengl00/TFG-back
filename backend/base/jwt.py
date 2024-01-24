from calendar import timegm
from datetime import datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from base.constants import CREATE_NEW_TOKEN_ERROR
from users.models import User

JWT_ACCESS_TYPE = "access"
JWT_REFRESH_TYPE = "refresh"
DEFAULT_AUTH_HEADER = "HTTP_AUTHORIZATION"
AUTH_HEADER_PREFIXES = ["JWT", "BEARER"]


def jwt_base_payload(exp_delta: timedelta | None) -> dict[str, Any]:
    utc_now = datetime.utcnow()
    payload = {"iat": utc_now}
    if exp_delta:
        payload["exp"] = utc_now + exp_delta
    return payload


def jwt_user_payload(
    user: User,
    token_type: str,
    exp_delta: timedelta | None,
) -> dict[str, Any]:
    payload = jwt_base_payload(exp_delta)
    payload.update(
        {
            "token": user.jwt_token_key,
            "email": user.email,
            "type": token_type,
            "user_id": str(user.id),
        }
    )
    return payload


def jwt_decode(token: dict[str, Any], verify_expiration=True) -> str:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_exp": verify_expiration},
    )


def jwt_encode(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def create_access_token(
    user: User, access_token_expires=settings.JWT_EXPIRE, override_ttl=None
) -> str:
    payload = jwt_user_payload(
        user,
        JWT_ACCESS_TYPE,
        settings.JWT_TTL_ACCESS_TIMEDELTA
        if access_token_expires and not override_ttl
        else override_ttl,
    )
    return jwt_encode(payload)


def create_refresh_token(
    user: User,
) -> str:
    payload = jwt_user_payload(
        user, JWT_REFRESH_TYPE, settings.JWT_TTL_REFRESH_TIMEDELTA
    )
    return jwt_encode(payload)


def get_user_from_payload(payload: dict[str, Any]) -> User | None:
    user = User.objects.filter(email__iexact=payload["email"], is_active=True).first()
    user_jwt_token = payload.get("token")
    if not user_jwt_token or not user:
        raise jwt.InvalidTokenError(CREATE_NEW_TOKEN_ERROR)
    if user.jwt_token_key != user_jwt_token:
        raise jwt.InvalidTokenError(CREATE_NEW_TOKEN_ERROR)
    orig_iat = payload.get("iat", 0)

    if user.logout and orig_iat < timegm(user.logout.utctimetuple()):
        raise jwt.InvalidTokenError(CREATE_NEW_TOKEN_ERROR)
    return user


def get_user_from_access_payload(payload: dict) -> User | None:
    jwt_type = payload.get("type")
    if jwt_type not in [
        JWT_ACCESS_TYPE,
    ]:
        raise jwt.InvalidTokenError(CREATE_NEW_TOKEN_ERROR)
    user = get_user_from_payload(payload)
    return user


def get_user_from_access_token(token: str) -> User | None:
    payload = jwt_decode(token)
    return get_user_from_access_payload(payload)


def get_token_from_request(request: WSGIRequest) -> str | None:
    auth = request.META.get(DEFAULT_AUTH_HEADER, "").split(maxsplit=1)
    if len(auth) == 2 and auth[0].upper() in AUTH_HEADER_PREFIXES:
        return auth[1]
    return None
