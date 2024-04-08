from datetime import datetime, timedelta

import pytz
import strawberry
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from base.graphql.inputs import PaginationInput
from base.graphql.utils import get_paginator
from resources.models import DayAvailability, Resource
from slots.graphql.inputs import GetSlotsInput
from slots.graphql.types import PaginatedReservedSlotType, SlotType
from slots.models import ReservedSlot


@strawberry.type
class ReservedSlotQuery:
    @strawberry.field(description="Returns a list of your reserved slots.")
    @login_required
    def my_reserved_slots(
        self, info: Info, pagination: PaginationInput | None = None
    ) -> PaginatedReservedSlotType:
        if pagination is None:
            pagination = {}
        user = info.context.request.user
        query = ReservedSlot.objects.filter(resource__user=user).order_by("-created")

        return get_paginator(
            query,
            pagination.page_size,
            pagination.page,
            PaginatedReservedSlotType,
        )

    @strawberry.field(description="Return an array of slots for a day")
    def get_slots(self, input: GetSlotsInput) -> list[SlotType]:
        resource = Resource.objects.get(id=input.resource_id)
        available_time = resource.available_time

        availabilities = DayAvailability.objects.filter(
            resource=resource, day=input.day
        ).order_by("start_time")

        reserved_slots = ReservedSlot.objects.filter(
            resource=resource, start_time__date=input.day
        )

        utc = pytz.UTC

        slots = []
        for availability in availabilities:
            # crear datetime
            start_time = datetime.combine(
                availability.day, availability.start_time
            ).replace(tzinfo=utc)
            end_time = datetime.combine(
                availability.day, availability.end_time
            ).replace(tzinfo=utc)

            last_possible_slot_end_time = end_time - timedelta(minutes=available_time)

            current_time = start_time
            while current_time <= last_possible_slot_end_time:
                slot_end_time = current_time + timedelta(minutes=available_time)

                is_reserved = any(
                    current_time < reserved_slot.end_time
                    and slot_end_time > reserved_slot.start_time
                    for reserved_slot in reserved_slots
                )

                slots.append(
                    SlotType(
                        start_time=current_time.time(),
                        end_time=slot_end_time.time(),
                        reserved=is_reserved,
                    )
                )

                current_time = slot_end_time
        return slots
