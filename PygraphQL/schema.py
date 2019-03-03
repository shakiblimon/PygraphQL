import graphene
import graphql_jwt
import testapp.schema_relay
import testapp.schema
import users.schema

class Query(testapp.schema.Query, users.schema.Query,testapp.schema_relay.RelayQuery, graphene.ObjectType):
    # as we begin to add more apps to this project
    pass

class Mutation(testapp.schema.Mutation, users.schema.Mutation, testapp.schema_relay.RelayMutation, graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query,mutation = Mutation)