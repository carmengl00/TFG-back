import json

import pytest
from mixer.backend.django import mixer

from base.factory_test_case import TestBase
from resources.errors import TIME_ERROR
from resources.models import DayAvailability, Resource
from resources.tests.requests.mutations import (
    CREATE_DAY_AVAILABILITY,
    DELETE_DAY_AVAILABILITY,
    UPDATE_DAY_AVAILABILITY,
)
from users.models import User


@pytest.mark.django_db()
class TestDayAvailabilityMutations(TestBase):
    def test_create_day_availability(self):
        resource = mixer.blend(Resource, start_date="2030-01-01", end_date="2030-03-01")

        variables = {
            "resourceId": resource.id,
            "input": {
                "day": "2030-02-04",
                "startTime": "10:00:00",
                "endTime": "13:00:00",
            },
        }
        response = self.post(
            query=CREATE_DAY_AVAILABILITY, variables=variables, user=self.user
        )

        data = json.loads(response.content.decode())

        day_availability = data.get("data")
        assert len(day_availability) == 1
        assert (
            day_availability.get("createDayAvailability").get("resource").get("name")
            == resource.name
        )

    def test_create_day_availability_time_error(self):
        resource = mixer.blend(Resource, start_date="2030-01-01", end_date="2030-03-01")

        variables = {
            "resourceId": resource.id,
            "input": {
                "day": "2030-02-04",
                "startTime": "10:00:00",
                "endTime": "09:00:00",
            },
        }
        response = self.post(
            query=CREATE_DAY_AVAILABILITY, variables=variables, user=self.user
        )
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == TIME_ERROR

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

    def test_update_day_availability(self):
        resource = mixer.blend(Resource, start_date="2030-01-01", end_date="2030-03-01")
        day_availability = mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-02",
            start_time="08:00:00",
            end_time="15:00:00",
        )
        variables = {
            "input": {
                "dayAvailabilityId": str(day_availability.id),
                "startTime": "09:00:00",
                "endTime": "13:00:00",
            }
        }
        response = self.post(
            query=UPDATE_DAY_AVAILABILITY, variables=variables, user=self.user
        )
        data = json.loads(response.content.decode())
        update = data.get("data").get("updateDayAvailability")
        assert update.get("startTime") == "09:00:00"
        assert update.get("endTime") == "13:00:00"

    def test_update_day_availability_time_error(self):
        day_availability = mixer.blend(
            DayAvailability, start_time="08:00:00", end_time="15:00:00"
        )
        variables = {
            "input": {
                "dayAvailabilityId": str(day_availability.id),
                "startTime": "09:00:00",
                "endTime": "08:00:00",
            }
        }
        response = self.post(
            query=UPDATE_DAY_AVAILABILITY, variables=variables, user=self.user
        )
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == TIME_ERROR
