import json

import pytest
from mixer.backend.django import mixer

from base.factory_test_case import TestBase
from resources.models import DayAvailability, Resource
from resources.tests.requests.queries import DAY_AVAILABILITY_ITEMS


@pytest.mark.django_db()
class TestResourcesQueries(TestBase):
    def test_my_daily_availabilities(self):
        resource = mixer.blend(Resource, user=self.user)
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-02",
            start_time="09:00:00",
            end_time="13:00:00",
        )
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-02-10",
            start_time="09:00:00",
            end_time="14:00:00",
        )
        mixer.blend(
            DayAvailability,
            resource=resource,
            day="2030-03-20",
            start_time="08:00:00",
            end_time="13:00:00",
        )

        variables = {
            "input": {
                "resourceId": resource.id,
                "year": 2030,
                "month": 2,
            },
        }

        response = self.post(
            query=DAY_AVAILABILITY_ITEMS, user=self.user, variables=variables
        )

        data = json.loads(response.content.decode())
        resources = data.get("data").get("myDailyAvailability")
        assert len(resources) == 2

        assert resources[0].get("day") == "2030-02-02"
        assert resources[1].get("availabilities")[0].get("startTime") == "09:00:00"
