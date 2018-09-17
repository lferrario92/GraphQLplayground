import graphene

from ingredients.schema import (
    Query as IngredientsQuery,
    Mutation as IngredientsMutation,
)


class Query(IngredientsQuery, graphene.ObjectType):
    """
    This class will inherit from multiple Query Objects from other
    projects as we begin to add more apps to our it and expose graphql
    nodes then.
    """
    pass


class Mutation(IngredientsMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
