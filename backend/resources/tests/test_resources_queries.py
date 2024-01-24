import json

import pytest
from mixer.backend.django import mixer

from base.factory_test_case import TestBase
from resources.models import Resource
from resources.tests.requests.queries import RESOURCES_ITEMS


@pytest.mark.django_db()
class TestResourcesQueries(TestBase):
    def test_my_resources(self):
        mixer.blend(
            Resource,
            user=self.user,
            name="Test 1",
            availableTime=30,
            location="Sevilla",
        )
        mixer.blend(
            Resource,
            user=self.user,
            name="Test 2",
            description="Test 2 prueba",
            availableTime=60,
            location="Aracena",
        )
        mixer.blend(
            Resource, user=self.user, name="Test 3", availableTime=120, location="Cádiz"
        )

        variables = {
            "pagination": {
                "page": 1,
                "pageSize": 5,
            },
        }

        response = self.post(query=RESOURCES_ITEMS, user=self.user, variables=variables)

        data = json.loads(response.content.decode())
        resources = data.get("data").get("myResources").get("edges")
        assert len(resources) == 3

        assert resources[0].get("name") == "Test 3"
        assert resources[1].get("description") == "Test 2 prueba"
        assert resources[2].get("location") == "Sevilla"

    def test_my_resources_without_pagination(self):
        mixer.blend(
            Resource,
            user=self.user,
            name="Test 1",
            availableTime=30,
            location="Sevilla",
        )
        mixer.blend(
            Resource,
            user=self.user,
            name="Test 2",
            description="Test 2 prueba",
            availableTime=60,
            location="Aracena",
        )
        mixer.blend(
            Resource, user=self.user, name="Test 3", availableTime=120, location="Cádiz"
        )

        variables = {}

        response = self.post(query=RESOURCES_ITEMS, user=self.user, variables=variables)
        data = json.loads(response.content.decode())
        assert data.get("data") is None
