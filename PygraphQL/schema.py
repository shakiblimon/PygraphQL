import graphene

import testapp.schema


class Query(testapp.schema.Query, graphene.ObjectType):
    # as we begin to add more apps to this project
    pass

schema = graphene.Schema(query=Query)