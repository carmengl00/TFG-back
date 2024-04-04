import json

import pytest
from mixer.backend.django import mixer

from base.factory_test_case import TestBase
from resources.models import Resource
from resources.tests.requests.queries import (
    RESOURCE_FROM_PUBLIC_NAME_ITEM,
    RESOURCE_ITEM,
    RESOURCES_ITEMS,
)
from users.models import User


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

    def test_resource(self):
        user = mixer.blend(User)
        resource = mixer.blend(
            Resource, user=user, name="Test 1", description="Descripción test 1"
        )
        variables = {"id": str(resource.id)}

        response = self.post(query=RESOURCE_ITEM, user=user, variables=variables)
        data = json.loads(response.content.decode())
        resource = data.get("data").get("resource")
        self.assertIsNotNone(resource)
        assert resource.get("name") == "Test 1"

    def test_resource_from_public_name(self):
        user = mixer.blend(
            User, public_name="pepito", first_name="Pepe", last_name="Grillo"
        )

        mixer.blend(Resource, user=user, name="Test 1")
        variables = {"publicName": "pepito"}

        response = self.post(
            query=RESOURCE_FROM_PUBLIC_NAME_ITEM, user=user, variables=variables
        )
        data = json.loads(response.content.decode())

        resource_data_list = data.get("data").get("resourceFromPublicName")

        retrieved_resource = resource_data_list[0]
        assert (
            retrieved_resource.get("name") == "Test 1"
        ), "El nombre del recurso no coincide"
