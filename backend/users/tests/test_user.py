import json
import secrets
from unittest.mock import patch

import jwt
import pytest
from django.conf import settings
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer
from strawberry.django.views import GraphQLView

from backend.schema import schema
from users.models import User
from users.utils import get_url_reset_password

ME = """
    query me {
        me {
            id
            token
        }
    }
"""

CHANGE_PASSWORD = """
mutation changePassword ($input: ChangePasswordInput!) {
    changePassword(input: $input)
}
"""

PROFILE = """
mutation user ($input: ProfileInput!) {
    user(input: $input) {
        firstName
        lastName
    }
}
"""

RESET_PASSWORD = """
mutation resetPassword ($input: ResetPasswordInput!) {
    resetPassword(input: $input)
}
"""

LOGIN = """
mutation login ($input: LoginInput!) {
    login(input: $input) {
        user{
            id
            email
        }
        token
        refreshToken
    }

}
"""

REGISTER = """
mutation register ($input: RegisterInput!) {
    register(input: $input) {
        firstName
        lastName
        publicName
        email
    }
}
"""

REQUEST_RESET_PASSWORD = """
mutation requestResetPassword ($input: RequestResetPasswordInput!) {
    requestResetPassword(input: $input)
}
"""

FAKE_ID = "12345678-1234-5678-1234-567812345678"


@pytest.mark.django_db()
class TestUserSchema(TestCase):
    CORRECT_EMAIL = "test@test.com"
    CORRECT_PASSWORD = "q&YsAp-Y8)KYd.H^"
    CORRECT_FIRST_NAME = "firstName"
    CORRECT_PUBLIC_NAME = "publicName"
    WRONG_FIRST_NAME = secrets.token_hex(31)
    CORRECT_LAST_NAME = "lastName"
    SHORT_PASSWORD = "short"
    COMMON_PASSWORD = "password"
    RESET_TOKEN = "eKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = mixer.blend(User, email="user@test.com")
        self.user.set_password(self.CORRECT_PASSWORD)
        self.user.save()

    def test_me(self):
        request = self.request_factory.post(
            "/graphql/", {"query": ME}, content_type="application/json"
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        me = data.get("data").get("me")
        assert me.get("id") == str(self.user.id)

    def test_register_correct(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": REGISTER,
                "variables": {
                    "input": {
                        "email": self.CORRECT_EMAIL,
                        "publicName": self.CORRECT_PUBLIC_NAME,
                        "firstName": self.CORRECT_FIRST_NAME,
                        "lastName": self.CORRECT_LAST_NAME,
                        "password": self.CORRECT_PASSWORD,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        register = data.get("data").get("register")
        assert register.get("firstName") == "firstName"
        assert register.get("lastName") == "lastName"
        assert register.get("publicName") == "publicName"
        assert register.get("email") == "test@test.com"

    def test_register_incorrect_email_already_exists(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": REGISTER,
                "variables": {
                    "input": {
                        "email": self.user.email,
                        "firstName": self.CORRECT_FIRST_NAME,
                        "lastName": self.CORRECT_LAST_NAME,
                        "publicName": self.CORRECT_PUBLIC_NAME,
                        "password": self.CORRECT_PASSWORD,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        errors = data.get("errors")
        assert errors[0].get("message") == "A user with that email already exists."

    def test_register_incorrect_short_password(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": REGISTER,
                "variables": {
                    "input": {
                        "email": self.CORRECT_EMAIL,
                        "firstName": self.CORRECT_FIRST_NAME,
                        "lastName": self.CORRECT_LAST_NAME,
                        "publicName": self.CORRECT_PUBLIC_NAME,
                        "password": self.SHORT_PASSWORD,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        errors = data.get("errors")
        assert (
            errors[0].get("message")
            == "This password is too short. It must contain at least 8 characters."
        )

    def test_register_incorrect_common_password(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": REGISTER,
                "variables": {
                    "input": {
                        "email": self.CORRECT_EMAIL,
                        "firstName": self.CORRECT_FIRST_NAME,
                        "lastName": self.CORRECT_LAST_NAME,
                        "publicName": self.CORRECT_PUBLIC_NAME,
                        "password": self.COMMON_PASSWORD,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        errors = data.get("errors")
        assert errors[0].get("message") == "This password is too common."

    def test_register_incorrect_empty_fields(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": REGISTER,
                "variables": {
                    "input": {
                        "email": "",
                        "firstName": "",
                        "lastName": "",
                        "publicName": "",
                        "password": self.CORRECT_PASSWORD,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        errors = data.get("errors")
        assert errors[0].get("message") == "All fields must be filled."

    def test_login(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": LOGIN,
                "variables": {
                    "input": {
                        "email": "user@test.com",
                        "password": self.CORRECT_PASSWORD,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        login = data.get("data").get("login")
        assert login.get("user").get("id") == str(self.user.id)
        assert login.get("user").get("email") == "user@test.com"

    def test_profile(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": PROFILE,
                "variables": {
                    "input": {
                        "firstName": self.CORRECT_FIRST_NAME,
                        "lastName": self.CORRECT_LAST_NAME,
                    }
                },
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        profile = data.get("data").get("user")
        assert profile.get("firstName") == "firstName"
        assert profile.get("lastName") == "lastName"

    def test_reset_password_correct(self):
        encoded_token = jwt.encode(
            {"user_id": str(self.user.id)}, settings.SECRET_KEY, algorithm="HS256"
        )
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": RESET_PASSWORD,
                "variables": {
                    "input": {
                        "token": encoded_token,
                        "password": self.CORRECT_PASSWORD,
                        "repeatPassword": None,
                    }
                },
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        assert data.get("data").get("resetPassword") is True

    def test_change_password_correct(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CHANGE_PASSWORD,
                "variables": {
                    "input": {
                        "currentPassword": self.CORRECT_PASSWORD,
                        "password": self.CORRECT_PASSWORD,
                        "repeatPassword": None,
                    }
                },
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        assert data.get("data").get("changePassword") is True

    def test_change_password_incorrect_current(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": CHANGE_PASSWORD,
                "variables": {
                    "input": {
                        "currentPassword": self.SHORT_PASSWORD,
                        "password": self.CORRECT_PASSWORD,
                        "repeatPassword": None,
                    }
                },
            },
            content_type="application/json",
        )
        request.user = self.user
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        errors = data.get("errors")
        assert errors[0].get("message") == "The current password is incorrect."

    def test_request_reset_password(self):
        request = self.request_factory.post(
            "/graphql/",
            {
                "query": REQUEST_RESET_PASSWORD,
                "variables": {"input": {"email": self.user.email}},
            },
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        data = json.loads(response.content.decode())
        assert data.get("data").get("requestResetPassword") is True

    @patch("jwt.encode", autospec=True)
    def test_get_url_secret_password(self, jwt_encode):
        url = get_url_reset_password(self.user.id, self.RESET_TOKEN)
        assert "reset-password" in url

    def test_manager_create_user(self):
        User.objects.create_user(
            email=self.CORRECT_EMAIL, password=self.CORRECT_PASSWORD
        )
        user = User.objects.filter(email=self.CORRECT_EMAIL)
        assert int(user.count()) == 1

    def test_manager_create_user_random_password(self):
        User.objects.create_user_random_password(email=self.CORRECT_EMAIL)
        user = User.objects.filter(email=self.CORRECT_EMAIL)
        assert int(user.count()) == 1

    def test_manager_create_super_user(self):
        User.objects.create_superuser(
            email=self.CORRECT_EMAIL, password=self.CORRECT_PASSWORD
        )
        user = User.objects.filter(email=self.CORRECT_EMAIL)
        assert int(user.count()) == 1

    def test_user_clean_email_already_exists(self):
        User.objects.create_user_random_password(email=self.CORRECT_EMAIL)
        user = User.objects.filter(email=self.CORRECT_EMAIL).first()
        with pytest.raises(Exception):
            user.clean_email()

    def test_filter_active_users(self):
        assert int(User.objects.filter_active().count()) == 1
