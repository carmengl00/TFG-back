from datetime import date, time
from uuid import UUID

import strawberry


@strawberry.input
class GetSlotsInput:
    resource_id: UUID
    day: date


@strawberry.input
class CreateReservedSlotInput:
    resource_id: UUID
    name: str
    description: str
    email: str
    day: date
    start_time: time
    end_time: time

@strawberry.input
class SendEmailReservationInput:
    email: str
    resource_name: str
    resource_description: str
    available_time: str
    location: str
    start_time: time
    end_time: time
    name: str
    description: str
    admin_email: str