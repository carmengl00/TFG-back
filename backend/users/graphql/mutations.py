import jwt
import strawberry
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils import timezone
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required
from strawberry_django_jwt.shortcuts import get_token

from base.utils import send_mail
from users import utils as users_utils
from users.graphql.inputs import (
    ChangePasswordInput,
    LoginInput,
    ProfileInput,
    RegisterInput,
    RequestResetPasswordInput,
    ResetPasswordInput,
)
from users.graphql.types import UserType
from users.models import User


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, input: RegisterInput) -> UserType:
        email = input.email.lower()
        if not email or not input.first_name or not input.last_name:
            raise Exception("All fields must be filled.")
        if User.objects.filter(email=email).exists():
            raise Exception("A user with that email already exists.")
        try:
            password_validation.validate_password(input.password)
        except ValidationError as e:
            # Remove extra characteres before sending error message
            raise Exception(str(e).replace("['", "").replace("']", ""))
        user = User(email=email, first_name=input.first_name, last_name=input.last_name)
        user.set_password(input.password)
        user.save()
        user.token = users_utils.get_token(user, input.password)
        return user

    @strawberry.mutation
    def login(self, info: Info, input: LoginInput) -> UserType:
        user = authenticate(
            request=info.context.request,
            username=input.email,
            password=input.password,
        )
        if user is None:
            raise Exception("Please, enter valid credentials")
        token = get_token(user, info.context)
        user.token = token
        user.last_login = timezone.now()
        user.save()
        return user

    @login_required
    @strawberry.mutation
    def user(self, info: Info, input: ProfileInput) -> UserType:
        user = info.context.request.user
        user.first_name = input.first_name
        user.last_name = input.last_name
        user.save()
        return user

    @login_required
    @strawberry.mutation
    def change_password(self, info: Info, input: ChangePasswordInput) -> bool:
        user = info.context.request.user
        if not user.check_password(input.current_password):
            raise Exception(
                "The current password is incorrect.",
            )
        if (
            input.password
            and input.repeat_password
            and input.password != input.repeat_password
        ):
            raise Exception(
                "The two password fields didn't match.",
            )
        try:
            password_validation.validate_password(input.password, user)
        except ValidationError as e:
            # Remove extra characteres before sending error message
            raise Exception(str(e).replace("['", "").replace("']", ""))
        user.set_password(input.password)
        user.save()
        return True

    @strawberry.mutation
    def request_reset_password(self, input: RequestResetPasswordInput) -> bool:
        user = User.objects.filter(email=input.email.lower()).first()
        if user:
            send_mail(
                subject_template_name="user/password_reset_subject.txt",
                email_template_name="user/password_reset_email.txt",
                context={
                    "email": user.email,
                    "reset_url": users_utils.get_url_reset_password(
                        user.pk, default_token_generator.make_token(user)
                    ),
                    "user": user,
                    "protocol": "https",
                },
                from_email=None,
                to_email=user.email,
                html_email_template_name="user/password_reset_email.html",
            )
        return True

    @strawberry.mutation
    def reset_password(self, input: ResetPasswordInput) -> bool:
        try:
            decoded_token = jwt.decode(
                input.token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise Exception("The token has expired")
        except jwt.InvalidTokenError:
            raise Exception("The token is invalid")
        except User.DoesNotExist:
            raise Exception("User does not exist")
        user = User.objects.get(id=decoded_token.get("user_id"))
        if (
            input.password
            and input.repeat_password
            and input.password != input.repeat_password
        ):
            raise Exception(
                "The two password fields didn't match.",
            )
        try:
            password_validation.validate_password(input.password, user)
        except ValidationError as e:
            # Remove extra characteres before sending error message
            raise Exception(str(e).replace("['", "").replace("']", ""))
        user.set_password(input.password)
        user.save()
        return True
