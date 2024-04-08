from datetime import date
from uuid import UUID

import strawberry


@strawberry.input
class GetSlotsInput:
    resource_id: UUID
    day: date
