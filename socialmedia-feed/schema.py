import graphene
import graphql_jwt
import feed.schema as feed_schema

class Query(feed_schema.Query, graphene.ObjectType):
    pass

class Mutation(feed_schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
