import graphene

import image.schema


class Query(image.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
