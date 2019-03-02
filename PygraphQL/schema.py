import graphene
from graphene_django.debug import DjangoDebug

import testapp.schema
from testapp.schema import Mutation


class Query(testapp.schema.Query, graphene.ObjectType):
    # as we begin to add more apps to this project
    pass

class Mutation(testapp.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation = Mutation)