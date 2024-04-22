import datetime

import strawberry

from resources.models import Resource
from slots.graphql.types import ReservedSlotType
from slots.models import ReservedSlot

from .inputs import CreateReservedSlotInput


@strawberry.type
class ReservedSlotMutation:
    @strawberry.field(description="Creates a resource")
    def create_reserved_slot(self, input: CreateReservedSlotInput) -> ReservedSlotType:
        resource = Resource.objects.get(id=input.resource_id)
        start_datetime = datetime.datetime.combine(input.day, input.start_time)
        end_datetime = datetime.datetime.combine(input.day, input.end_time)

        reserved_slot = ReservedSlot.objects.create(
            resource=resource,
            name=input.name,
            description=input.description,
            email=input.email,
            start_time=start_datetime,
            end_time=end_datetime,
        )
        return reserved_slot
