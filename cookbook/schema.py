import graphene

import cookbook.ingredients.schema


class Query(cookbook.ingredients.schema.Query, graphene.ObjectType):
    """
    This class will inherit from multiple Query Objects from other
    projects as we begin to add more apps to our it and expose graphql
    nodes then.
    """
    pass


schema = graphene.Schema(query=Query)
