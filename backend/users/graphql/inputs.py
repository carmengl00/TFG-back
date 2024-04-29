import strawberry


@strawberry.input
class RegisterInput:
    email: str
    public_name: str
    first_name: str
    last_name: str
    password: str


@strawberry.input
class LoginInput:
    email: str
    password: str


@strawberry.input
class ProfileInput:
    first_name: str
    last_name: str

@strawberry.input
class ProfileEditInput:
    first_name: str | None = strawberry.UNSET
    last_name: str | None = strawberry.UNSET
    email: str | None = strawberry.UNSET
    public_name: str | None = strawberry.UNSET


@strawberry.input
class ChangePasswordInput:
    current_password: str
    password: str
    repeat_password: str | None


@strawberry.input
class RequestResetPasswordInput:
    email: str


@strawberry.input
class ResetPasswordInput:
    token: str
    password: str
    repeat_password: str | None
