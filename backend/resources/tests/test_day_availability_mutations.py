import json

import pytest
from mixer.backend.django import mixer

from base.factory_test_case import TestBase
from resources.models import DayAvailability, Resource
from resources.tests.requests.mutations import (
    CREATE_OR_UPDATE_AVAILABILITY,
    DELETE_DAY_AVAILABILITY,
)
from users.models import User


@pytest.mark.django_db()
class TestDayAvailabilityMutations(TestBase):
    def test_create_or_update_availability(self):
        resource = mixer.blend(Resource, start_date="2030-01-01", end_date="2030-03-01")
        availability = mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-18",
            start_time="09:00",
            end_time="11:00",
        )
        variables = {
            "input": {
                "resourceId": str(resource.id),
                "items": [
                    {
                        "day": "2030-02-18",
                        "timeRange": [
                            {
                                "dayAvailabilityId": str(availability.id),
                                "startTime": "09:00",
                                "endTime": "12:00",
                            },
                            {
                                "startTime": "13:00",
                                "endTime": "14:00",
                            },
                        ],
                    },
                    {
                        "day": "2030-02-20",
                        "timeRange": [
                            {
                                "startTime": "09:00",
                                "endTime": "12:00",
                            }
                        ],
                    },
                ],
            },
        }
        response = self.post(
            query=CREATE_OR_UPDATE_AVAILABILITY, variables=variables, user=self.user
        )

        data = json.loads(response.content.decode())

        day_availability = data.get("data")
        assert len(day_availability) == 1
        assert day_availability.get("createOrUpdateAvailability") is True

    def test_delete_day_availability(self):
        day_availability = mixer.blend(DayAvailability)
        variables = {
            "id": str(day_availability.id),
        }
        response = self.post(
            query=DELETE_DAY_AVAILABILITY, variables=variables, user=self.user
        )
        data = json.loads(response.content.decode())
        day_availability = data.get("data").get("deleteDayAvailability")
        assert day_availability is True

    def test_delete_another_users_day_availability(self):
        user = mixer.blend(User)
        resource = mixer.blend(Resource, user=user)
        day_availability = mixer.blend(DayAvailability, resource=resource)
        variables = {
            "id": str(day_availability.id),
        }
        self.post(
            query=DELETE_DAY_AVAILABILITY,
            variables=variables,
        )
        assert len(DayAvailability.objects.all()) == 1
