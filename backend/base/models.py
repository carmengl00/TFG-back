import uuid
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:  # pragma: no cover
    import datetime  # NOQA


class SimpleModel(models.Model):
    """
    An abstract base class model that provides:
    self-updating 'created' and 'modified' fields.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )  # type: uuid.UUID

    created = models.DateTimeField(
        verbose_name=_("created date"),
        null=True,
        auto_now_add=True,
    )  # type: datetime.datetime
    modified = models.DateTimeField(
        verbose_name=_("modified date"), null=True, auto_now=True
    )  # type: datetime.datetime

    class Meta:
        abstract = True
        ordering = ("-created",)
