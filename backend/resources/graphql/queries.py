import strawberry
from strawberry.types import Info
from strawberry_django_jwt.decorators import login_required

from base.graphql.inputs import PaginationInput
from base.graphql.utils import get_paginator
from resources.graphql.inputs import MonthInput
from resources.graphql.types import PaginatedDayAvailabilityType, PaginatedResourceType
from resources.models import DayAvailability, Resource


@strawberry.type
class ResourcesQuery:
    @strawberry.field(description="Returns a list of your resources.")
    @login_required
    def my_resources(
        self, info: Info, pagination: PaginationInput | None = None
    ) -> PaginatedResourceType:
        if pagination is None:
            pagination = {}
        user = info.context.request.user
        query = Resource.objects.filter(user=user).order_by("-created")

        return get_paginator(
            query,
            pagination.page_size,
            pagination.page,
            PaginatedResourceType,
        )

    @strawberry.field(description="Returns a list of your daily availabilities.")
    @login_required
    def my_daily_availability(
        self, info: Info, input: MonthInput, pagination: PaginationInput | None = None
    ) -> PaginatedDayAvailabilityType:
        if pagination is None:
            pagination = {}
        user = info.context.request.user
        resources = Resource.objects.filter(user=user)
        query = DayAvailability.objects.filter(
            resource__in=resources, day__year=input.year, day__month=input.month
        ).order_by("day", "start_time")

        return get_paginator(
            query, pagination.page_size, pagination.page, PaginatedDayAvailabilityType
        )
