import strawberry
from strawberry_django_jwt.middleware import JSONWebTokenMiddleware

from media_upload.graphql.mutations import Mutation as MediaUploadMutation
from users.graphql.mutations import Mutation as UsersMutation
from users.graphql.queries import Query as UsersQuery


@strawberry.type
class Mutation(UsersMutation, MediaUploadMutation):
    pass


@strawberry.type
class Query(UsersQuery):
    pass


schema = strawberry.Schema(
    query=Query, mutation=Mutation, extensions=[JSONWebTokenMiddleware]
)
