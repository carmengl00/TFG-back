import strawberry


@strawberry.input
class PaginationInput:
    page: int | None
    page_size: int | None
