import strawberry
from strawberry_django_jwt.middleware import JSONWebTokenMiddleware

from media_upload.graphql.mutations import Mutation as MediaUploadMutation
from resources.graphql.mutations import ResourceMutation
from resources.graphql.queries import ResourcesQuery
from slots.graphql.queries import ReservedSlotQuery
from users.graphql.mutations import Mutation as UsersMutation
from users.graphql.queries import Query as UsersQuery


@strawberry.type
class Mutation(UsersMutation, MediaUploadMutation, ResourceMutation):
    pass


@strawberry.type
class Query(UsersQuery, ResourcesQuery, ReservedSlotQuery):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[JSONWebTokenMiddleware]
)
