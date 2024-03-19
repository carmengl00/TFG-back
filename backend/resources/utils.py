from django.core.exceptions import ValidationError

from base.exceptions import AvailabilityValidationException
from resources.errors import OVERLAP_ERROR
from resources.graphql.inputs import CreateOrUpdateAvailabilityInput


def validate_input(input: CreateOrUpdateAvailabilityInput):
    for day_availability_input in input.items:
        seen_time_ranges = []
        day = day_availability_input.day
        for time_range_input in day_availability_input.timeRange:
            start_time = time_range_input.start_time
            end_time = time_range_input.end_time

            # Repetitions and overlap validation
            for existing_time_range in seen_time_ranges:
                if (
                    start_time < existing_time_range[1]
                    and end_time > existing_time_range[0]
                ):
                    raise AvailabilityValidationException(
                        OVERLAP_ERROR,
                        conflicting_day=day,
                        conflicting_start_time=start_time,
                        conflicting_end_time=end_time,
                    )

            seen_time_ranges.append((start_time, end_time))


def overlapping(day_availabilities_dict, day, end_time, start_time):
    overlapping = False
    for existing_availability in day_availabilities_dict.values():
        if (
            existing_availability.day == day
            and existing_availability.start_time < end_time
            and existing_availability.end_time > start_time
        ):
            overlapping = True
            break

    if overlapping:
        raise ValidationError(OVERLAP_ERROR)
