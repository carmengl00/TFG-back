from datetime import time

import strawberry

from base.graphql.types import PaginatedQueryType
from resources.graphql.types import ResourceType


@strawberry.type
class ReservedSlotType:
    resource: ResourceType
    name: str
    description: str
    email: str
    start_time: time
    end_time: time


@strawberry.type
class SlotType:
    start_time: time
    end_time: time
    reserved: bool


@strawberry.type
class PaginatedReservedSlotType(PaginatedQueryType):
    edges: list[ReservedSlotType]
