from django.contrib import admin

from slots.models import ReservedSlot

# Register your models here.


@admin.register(ReservedSlot)
class ReservedSlotAdmin(admin.ModelAdmin):
    list_select_related = "resource"
    list_display = (
        "resource",
        "name",
        "description",
        "email",
        "start_time",
        "end_time",
    )
    list_filter = ("start_time", "end_time")
    ordering = ("start_time",)
    search_fields = ("resource", "name", "description", "email")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "resource",
                    "name",
                    "description",
                    "email",
                    "start_time",
                    "end_time",
                )
            },
        ),
    )
