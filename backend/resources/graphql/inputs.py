from datetime import date
from uuid import UUID

import strawberry


@strawberry.input
class ResourceInput:
    name: str
    description: str
    available_time: int
    start_date: date
    end_date: date
    location: str | None = strawberry.UNSET


@strawberry.input
class UpdateResourceInput:
    resource_id: UUID
    name: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    available_time: int | None = strawberry.UNSET
    start_date: date | None = strawberry.UNSET
    end_date: date | None = strawberry.UNSET
    location: str | None = strawberry.UNSET
