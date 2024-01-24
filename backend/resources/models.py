from datetime import date

from django.db import models

from base.models import SimpleModel


class Resource(SimpleModel):
    user = models.ForeignKey(
        "users.User",
        verbose_name="user",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="name",
        max_length=30,
    )
    description = models.CharField(
        verbose_name="description",
        max_length=100,
    )
    available_time = models.IntegerField(
        verbose_name="available_time",
        help_text="Maximum reservation time in minutes",
    )
    start_date = models.DateField(
        verbose_name="start_date",
        default=date.today,
    )
    end_date = models.DateField(
        verbose_name="end_date",
    )

    location = models.CharField(
        verbose_name="location", max_length=100, blank=True, null=True
    )

    class Meta:
        verbose_name = "resource"
        verbose_name_plural = "resources"
        ordering = ("start_date",)


class DayAvailability(SimpleModel):
    resource = models.ForeignKey(
        Resource,
        verbose_name="resource",
        on_delete=models.CASCADE,
    )

    day = models.DateField(
        verbose_name="day",
    )

    start_time = models.TimeField(
        verbose_name="start_time",
    )

    end_time = models.TimeField(
        verbose_name="end_time",
    )

    class Meta:
        verbose_name = "availability"
        verbose_name_plural = "availabilities"
        ordering = ("day",)
