from datetime import datetime, time

import strawberry

from base.graphql.types import PaginatedQueryType
from resources.graphql.types import ResourceType


@strawberry.type
class ReservedSlotType:
    resource: ResourceType
    id: str
    name: str
    description: str
    email: str
    start_time: datetime
    end_time: datetime


@strawberry.type
class SlotType:
    start_time: time
    end_time: time
    reserved: bool


@strawberry.type
class PaginatedReservedSlotType(PaginatedQueryType):
    edges: list[ReservedSlotType]
