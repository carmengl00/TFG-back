import uuid
from datetime import date

import strawberry

from base.graphql.types import PaginatedQueryType
from users.graphql.types import UserType


@strawberry.type
class ResourceType:
    user: UserType
    id: uuid.UUID
    name: str
    description: str
    available_time: int
    start_date: date
    end_date: date
    location: str | None


@strawberry.type
class PaginatedResourceType(PaginatedQueryType):
    edges: list[ResourceType]
