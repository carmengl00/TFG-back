from datetime import date, time
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
class TimeRangeInput:
    day_availability_id: UUID | None = strawberry.UNSET
    start_time: time
    end_time: time


@strawberry.input
class DayAvailabilityInput:
    day: date
    timeRange: list[TimeRangeInput]


@strawberry.input
class MonthInput:
    resource_id: UUID
    month: int
    year: int


@strawberry.input
class UpdateResourceInput:
    resource_id: UUID
    name: str | None = strawberry.UNSET
    description: str | None = strawberry.UNSET
    available_time: int | None = strawberry.UNSET
    start_date: date | None = strawberry.UNSET
    end_date: date | None = strawberry.UNSET
    location: str | None = strawberry.UNSET


@strawberry.input
class UpdateDayAvailabilityInput:
    day_availability_id: UUID
    start_time: time
    end_time: time


@strawberry.input
class CreateOrUpdateAvailabilityInput:
    resource_id: UUID
    items: list[DayAvailabilityInput]
