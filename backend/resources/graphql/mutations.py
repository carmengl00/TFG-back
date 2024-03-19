from uuid import UUID

import strawberry
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from base.exceptions import AvailabilityValidationException
from resources.errors import DATE_ERROR, EXISTING_RESOURCE, PAST_DATE, PERMISSION_ERROR
from resources.graphql.inputs import (
    CreateOrUpdateAvailabilityInput,
    ResourceInput,
    UpdateResourceInput,
)
from resources.graphql.types import ResourceType
from resources.models import DayAvailability, Resource
from resources.utils import overlapping, validate_input


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

    @strawberry.field(description="Delete a day availability")
    @login_required
    def delete_day_availability(self, id: UUID) -> bool:
        DayAvailability.objects.filter(id=id).delete()
        return True

    @strawberry.field(description="Creates or updates day availability")
    @login_required
    def create_or_update_availability(
        self,
        input: CreateOrUpdateAvailabilityInput,
    ) -> bool:
        try:
            # Validate input data.
            validate_input(input)

            # Get the availabilities of the resource
            # {day_availability_id:
            # DayAvailability(id, resource, day, startTime, endTime)}

            resource = Resource.objects.get(id=input.resource_id)
            day_availabilities_dict = {}
            day_availabilities = DayAvailability.objects.filter(resource_id=resource.id)

            for item in day_availabilities:
                day_availabilities_dict[item.id] = item

            # Iterate through the TimeRange input,
            # declare empty lists to_create and to_update.
            # Check if the ID exists, ensuring it's in the previous step.
            to_update = []
            to_create = []

            for day_availability_input in input.items:
                for time_range_input in day_availability_input.timeRange:
                    day_availability_id = time_range_input.day_availability_id

                    if day_availability_id:
                        if day_availability_id in day_availabilities_dict:
                            value = day_availabilities_dict[day_availability_id]

                            value.start_time = time_range_input.start_time
                            value.end_time = time_range_input.end_time

                            day_availabilities_dict[day_availability_id] = value
                            to_update.append(value)
                        else:
                            raise ValidationError("Day availability does not exist.")
                    else:
                        # The ID does not exist, and the new input does not overlap
                        # with existing ones, so a new DayAvailability is created.

                        overlapping(
                            day_availabilities_dict,
                            day_availability_input.day,
                            time_range_input.end_time,
                            time_range_input.start_time,
                        )

                        new_day_availability_type = DayAvailability(
                            resource=resource,
                            day=day_availability_input.day,
                            start_time=time_range_input.start_time,
                            end_time=time_range_input.end_time,
                        )

                        to_create.append(new_day_availability_type)

            # bulk_update y bulk_create
            fields_to_update = ["start_time", "end_time", "modified"]
            DayAvailability.objects.bulk_update(to_update, fields_to_update)
            DayAvailability.objects.bulk_create(to_create)
        except AvailabilityValidationException as e:
            print(
                f"An error occurred: {e}, "
                f"{e.conflicting_day}, "
                f"{e.conflicting_start_time}, "
                f"{e.conflicting_end_time}"
            )
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            return True
