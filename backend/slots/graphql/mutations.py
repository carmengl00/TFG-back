import datetime
from uuid import UUID

import strawberry

from resources.models import Resource
from slots.graphql.types import ReservedSlotType
from slots.models import ReservedSlot
from strawberry_django_jwt.decorators import login_required

from .inputs import CreateReservedSlotInput


@strawberry.type
class ReservedSlotMutation:
    @strawberry.field(description="Creates a reserved slot")
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
    
    @strawberry.field(description="Deletes a reserved slot")
    @login_required
    def delete_reserved_slot(self, id: UUID) -> bool:
        ReservedSlot.objects.get(id=id).delete()
        return True
