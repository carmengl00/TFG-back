import strawberry
from django.utils import timezone
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from users.graphql.types import UserType


@strawberry.type
class Query:
    @login_required
    @strawberry.field
    def me(self, info: Info) -> UserType:
        user = info.context.request.user
        user.last_login = timezone.now()
        user.save()
        return user
