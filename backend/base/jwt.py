from datetime import datetime, timedelta
from typing import Any

import jwt
from django.conf import settings

from users.models import User

JWT_ACCESS_TYPE = "access"
JWT_REFRESH_TYPE = "refresh"


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
