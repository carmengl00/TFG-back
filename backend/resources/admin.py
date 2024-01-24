from django.contrib import admin
from django.contrib.admin import ModelAdmin

from resources.models import DayAvailability, Resource

# Register your models here.


@admin.register(Resource)
class ResourceAdmin(ModelAdmin):
    list_display = (
        "name",
        "description",
        "available_time",
        "start_date",
        "end_date",
        "location",
    )
    list_filter = ("start_date", "end_date")
    ordering = ("start_date",)
    search_fields = ("name", "description")

    fieldsets = (
        (None, {"fields": ("name", "description", "available_time", "location")}),
        (
            "Date information",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "User information",
            {"fields": ("user",)},
        ),
    )


@admin.register(DayAvailability)
class DayAvailabilityAdmin(ModelAdmin):
    list_display = (
        "resource",
        "day",
        "start_time",
        "end_time",
    )
    list_filter = ("day",)
    ordering = ("day",)
    search_fields = ("resource",)

    fieldsets = ((None, {"fields": ("resource", "day", "start_time", "end_time")}),)
