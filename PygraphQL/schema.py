import graphene
from graphene_django.debug import DjangoDebug

import testapp.schema


class Query(testapp.schema.Query, graphene.ObjectType):
    # as we begin to add more apps to this project
    debug= graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query)