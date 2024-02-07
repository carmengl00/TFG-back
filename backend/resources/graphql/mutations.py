from uuid import UUID

import strawberry
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.utils import timezone
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from resources.errors import (
    DATE_ERROR,
    EXISTING_RESOURCE,
    OUT_OF_RANGE,
    OVERLAP_ERROR,
    PAST_DATE,
    PERMISSION_ERROR,
    TIME_ERROR,
)
from resources.graphql.inputs import (
    DayAvailabilityInput,
    ResourceInput,
    UpdateDayAvailabilityInput,
    UpdateResourceInput,
)
from resources.graphql.types import DayAvailabilityType, ResourceType
from resources.models import DayAvailability, Resource


@strawberry.type
class ResourceMutation:
    @strawberry.field(description="Creates a resource")
    @login_required
    def create_resource(self, input: ResourceInput, info: Info) -> ResourceType:
        user = info.context.request.user
        if input.start_date < timezone.now().date():
            raise ValidationError(PAST_DATE)

        if input.start_date >= input.end_date:
            raise ValidationError(DATE_ERROR)

        existing_resource = Resource.objects.filter(
            user=user,
            name=input.name,
            start_date=input.start_date,
            end_date=input.end_date,
            available_time=input.available_time,
        ).first()
        if existing_resource:
            raise ValidationError(EXISTING_RESOURCE)

        location_value = input.location if input.location != strawberry.UNSET else None

        resource = Resource.objects.create(
            user=user,
            name=input.name,
            description=input.description,
            available_time=input.available_time,
            start_date=input.start_date,
            end_date=input.end_date,
            location=location_value,
        )

        return resource

    @strawberry.field(description="Delete your resource")
    @login_required
    def delete_resource(self, id: UUID, info: Info) -> bool:
        user = info.context.request.user
        resource = Resource.objects.filter(id=id, user=user)
        if not resource:
            raise PermissionDenied("You do not have permission to perform this action.")
        resource.delete()
        return True

    @strawberry.field(description="Updates a resource")
    @login_required
    def update_resource(self, input: UpdateResourceInput, info: Info) -> ResourceType:
        user = info.context.request.user
        resource = Resource.objects.filter(user=user, id=input.resource_id).first()
        if not resource:
            raise ValidationError(PERMISSION_ERROR)

        updated_fields = {
            "name": resource.name if input.name == strawberry.UNSET else input.name,
            "description": resource.description
            if input.description == strawberry.UNSET
            else input.description,
            "available_time": resource.available_time
            if input.available_time == strawberry.UNSET
            else input.available_time,
            "start_date": resource.start_date
            if input.start_date == strawberry.UNSET
            else input.start_date,
            "end_date": resource.end_date
            if input.end_date == strawberry.UNSET
            else input.end_date,
            "location": resource.location
            if input.location == strawberry.UNSET
            else input.location,
        }

        if input.start_date and input.start_date < timezone.now().date():
            raise ValidationError(PAST_DATE)

        if updated_fields["start_date"] >= updated_fields["end_date"]:
            raise ValidationError(DATE_ERROR)

        existing_resource = Resource.objects.filter(
            user=user,
            name=updated_fields["name"],
            start_date=updated_fields["start_date"],
            end_date=updated_fields["end_date"],
            available_time=updated_fields["available_time"],
        ).first()
        if existing_resource:
            raise ValidationError(EXISTING_RESOURCE)

        resource.name = updated_fields["name"]
        resource.description = updated_fields["description"]
        resource.available_time = updated_fields["available_time"]
        resource.start_date = updated_fields["start_date"]
        resource.end_date = updated_fields["end_date"]
        resource.location = updated_fields["location"]

        resource.save()

        return resource

    @strawberry.field(description="Creates a day availability")
    @login_required
    def create_day_availability(
        self, input: DayAvailabilityInput, resource_id: UUID
    ) -> DayAvailabilityType:
        resource = Resource.objects.get(id=resource_id)

        if input.day < resource.start_date or input.day > resource.end_date:
            raise ValidationError(OUT_OF_RANGE)

        if input.start_time >= input.end_time:
            raise ValidationError(TIME_ERROR)

        if DayAvailability.objects.filter(
            day=input.day,
            start_time__lt=input.end_time,
            end_time__gt=input.start_time,
        ).exists():
            raise ValidationError(OVERLAP_ERROR)

        day_availability = DayAvailability.objects.create(
            resource=resource,
            day=input.day,
            start_time=input.start_time,
            end_time=input.end_time,
        )

        return day_availability

    @strawberry.field(description="Delete a day availability")
    @login_required
    def delete_day_availability(self, id: UUID) -> bool:
        DayAvailability.objects.filter(id=id).delete()
        return True

    @strawberry.field(description="Updates a day availability")
    @login_required
    def update_day_availability(
        self, input: UpdateDayAvailabilityInput
    ) -> DayAvailabilityType:
        day_availability = DayAvailability.objects.get(id=input.day_availability_id)

        updated_fields = {
            "start_time": input.start_time,
            "end_time": input.end_time,
        }

        if input.start_time >= input.end_time:
            raise ValidationError(TIME_ERROR)

        if DayAvailability.objects.filter(
            ~Q(id=input.day_availability_id),
            day=day_availability.day,
            start_time__lt=input.end_time,
            end_time__gt=input.start_time,
        ).exists():
            raise ValidationError(OVERLAP_ERROR)

        day_availability.start_time = updated_fields["start_time"]
        day_availability.end_time = updated_fields["end_time"]

        day_availability.save()

        return day_availability
