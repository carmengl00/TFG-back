import uuid
from datetime import date, time

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
class DayAvailabilityType:
    id: uuid.UUID
    resource: ResourceType
    day: date
    start_time: time
    end_time: time


@strawberry.type
class PaginatedResourceType(PaginatedQueryType):
    edges: list[ResourceType]


@strawberry.type
class PaginatedDayAvailabilityType(PaginatedQueryType):
    edges: list[DayAvailabilityType]
