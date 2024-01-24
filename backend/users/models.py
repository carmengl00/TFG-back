import uuid
from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager

if TYPE_CHECKING:  # pragma: no cover
    import datetime  # NOQA


def generate_jwt_token() -> str:
    return get_random_string(12)


class User(AbstractBaseUser, PermissionsMixin):
    """Description: Customized User Model"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )  # type: uuid.UUID

    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=30,
        blank=True,
        null=True,
    )  # type: str
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=30,
        blank=True,
        null=True,
    )  # type: str

    public_name = models.CharField(
        verbose_name=_("public name"),
        max_length=30,
        unique=True,
        help_text=_("Visible name when users go to reserve your resource."),
    )  # type: str

    time_zone = models.DateTimeField(
        verbose_name=_("time zone"),
        default=timezone.now,
    )  # type: datetime.datetime
    password = models.CharField(_("password"), max_length=100)  # type: str
    # Email
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
    )  # type: str
    email_confirmed = models.BooleanField(
        verbose_name=_("email confirmed"), default=False
    )
    logout = models.DateTimeField(
        verbose_name=_("logout"), null=True, blank=True, editable=False
    )  # type: datetime.datetime
    # Internal
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Designates whether the user " "can log into this admin site."),
    )  # type: bool
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )  # type: bool
    created = models.DateTimeField(
        verbose_name=_("created date"),
        null=True,
        auto_now_add=True,
    )  # type: datetime.datetime
    modified = models.DateTimeField(
        verbose_name=_("modified date"),
        null=True,
        auto_now=True,
    )  # type: datetime.datetime

    jwt_token_key = models.CharField(max_length=12, default=generate_jwt_token)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def get_full_name(self):
        # type: () -> str
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        # type: () -> str
        return self.first_name

    def clean_email(self):
        # type: () -> None
        super().clean()
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)
            if self.__class__.objects.filter(email=self.email).exists():
                raise ValidationError(_("A user with that email already exists."))

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("first_name", "last_name")
