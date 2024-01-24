import pytest
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer
from strawberry.django.views import GraphQLView

from backend.schema import schema
from users.models import User


@pytest.mark.django_db()
class TestBase(TestCase):
    CORRECT_EMAIL = "test@test.com"
    ANOTHER_EMAIL = "test2@test.com"

    @classmethod
    def setUpClass(cls):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")

        super().setUpClass()

    def setUp(self) -> None:
        self.request_factory = RequestFactory()
        self.user = mixer.blend(User)
        self.url = "/graphql/"

    def post(self, query=None, variables=None, user=None):
        assert query is not None
        request = self.request_factory.post(
            self.url,
            {
                "query": query,
                "variables": variables,
            },
            content_type="application/json",
        )
        request.user = user

        return GraphQLView.as_view(schema=schema)(request)
