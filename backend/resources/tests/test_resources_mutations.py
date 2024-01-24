import json

import pytest
from mixer.backend.django import mixer
from strawberry.django.views import GraphQLView

from backend.schema import schema
from base.factory_test_case import TestBase
from resources.errors import DATE_ERROR, EXISTING_RESOURCE, PAST_DATE
from resources.models import Resource
from resources.tests.requests.mutations import (
    CREATE_RESOURCE,
    DELETE_RESOURCE,
    UPDATE_RESOURCE,
)
from users.models import User


@pytest.mark.django_db()
class TestResourcesMutations(TestBase):
    def test_create_resource(self):
        variables = {
            "input": {
                "name": "test 1",
                "description": "test 1 description",
                "availableTime": 120,
                "startDate": "2024-02-22",
                "endDate": "2024-02-27",
                "location": "Sevilla",
            }
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        user = User.objects.get(id=self.user.id)

        resource = data.get("data")
        assert len(resource) == 1
        assert resource.get("createResource").get("user").get("email") == user.email

    def test_create_resource_past_date(self):
        variables = {
            "input": {
                "name": "test 1",
                "description": "test 1 description",
                "availableTime": 120,
                "startDate": "2022-02-22",
                "endDate": "2024-02-27",
                "location": "Sevilla",
            }
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == PAST_DATE

    def test_create_resource_date_error(self):
        variables = {
            "input": {
                "name": "test 1",
                "description": "test 1 description",
                "availableTime": 120,
                "startDate": "2024-02-22",
                "endDate": "2024-02-20",
                "location": "Sevilla",
            }
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == DATE_ERROR

    def test_create_resource_existing_resource(self):
        mixer.blend(
            Resource,
            user=self.user,
            name="test 1",
            available_time=120,
            start_date="2030-02-22",
            end_date="2030-02-27",
        )
        variables = {
            "input": {
                "name": "test 1",
                "description": "test 1 description",
                "availableTime": 120,
                "startDate": "2030-02-22",
                "endDate": "2030-02-27",
                "location": "Sevilla",
            }
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CREATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == EXISTING_RESOURCE

    def test_delete_resource(self):
        resource = mixer.blend(
            Resource,
            user=self.user,
            name="Test 1",
            availableTime=30,
            location="Sevilla",
        )
        variables = {
            "id": str(resource.id),
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": DELETE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        resource = data.get("data").get("deleteResource")
        assert resource is True

    def test_delete_another_users_resource(self):
        user1 = mixer.blend(User)
        resource = mixer.blend(
            Resource,
            user=user1,
            name="Test 1",
            availableTime=30,
            location="Sevilla",
        )
        variables = {
            "id": str(resource.id),
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": DELETE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        assert (
            data.get("errors")[0].get("message")
            == "You do not have permission to perform this action."
        )

    def test_update_resource(self):
        resource = mixer.blend(
            Resource,
            user=self.user,
            name="Test 1",
            available_time=30,
            start_date="2030-02-02",
            end_date="2040-02-03",
            location="Sevilla",
        )
        variables = {
            "input": {
                "resourceId": str(resource.id),
                "name": "Test editado",
                "availableTime": 60,
                "location": "Huelva",
            }
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": UPDATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        update = data.get("data").get("updateResource")
        assert update.get("name") == "Test editado"
        assert update.get("availableTime") == 60
        assert update.get("location") == "Huelva"

    def test_update_resource_past_date(self):
        resource = mixer.blend(
            Resource,
            user=self.user,
            name="Test 1",
            availableTime=30,
            location="Sevilla",
        )
        variables = {
            "input": {"resourceId": str(resource.id), "startDate": "2022-01-01"}
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": UPDATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )

        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == PAST_DATE

    def test_update_resource_date_error(self):
        resource = mixer.blend(
            Resource,
            user=self.user,
            name="Test 1",
            availableTime=30,
            location="Sevilla",
        )
        variables = {
            "input": {
                "resourceId": str(resource.id),
                "startDate": "2040-02-01",
                "endDate": "2024-01-01",
            }
        }
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": UPDATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )

        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == DATE_ERROR

    def test_update_resource_existing_resource(self):
        resource = mixer.blend(
            Resource,
            user=self.user,
            name="Test 1",
            available_time=30,
            start_date="2025-01-01",
            end_date="2026-01-01",
            location="Sevilla",
        )
        variables = {"input": {"resourceId": str(resource.id), "name": "Test 1"}}
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": UPDATE_RESOURCE,
                "variables": variables,
            },
            content_type="application/json",
        )

        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())

        assert data.get("errors")[0].get("message") == EXISTING_RESOURCE
