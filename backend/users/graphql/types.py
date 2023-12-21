from datetime import datetime
from uuid import UUID

import strawberry
from strawberry.types import Info
from strawberry_django_jwt.settings import jwt_settings


@strawberry.type
class UserType:
    id: UUID
    first_name: str
    last_name: str
    email: str
    public_name: str
    created: datetime

    @strawberry.field
    def token(self, info: Info) -> str:
        if hasattr(self, "token"):
            return self.token
        auth = info.context.request.META.get(
            jwt_settings.JWT_AUTH_HEADER_NAME, ""
        ).split()
        prefix = jwt_settings.JWT_AUTH_HEADER_PREFIX
        if len(auth) == 2 and auth[0].lower() == prefix.lower():
            return auth[1]
        return ""


@strawberry.type
class UserTypeWeb:
    user: UserType
    token: str
    refresh_token: str
