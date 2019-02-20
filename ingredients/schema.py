import graphene

from graphene_django.types import DjangoObjectType

from ingredients.models import Category, Ingredient
from forms import IngredientForm


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class AnyType(graphene.Scalar):
    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_value(value):
        return value

    @staticmethod
    def parse_literal(ast):
        return ast.value


class Query(object):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()


class CreateIngredientMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        notes = graphene.String()
        category = graphene.ID()

    ok = graphene.Boolean()
    errors = AnyType()
    ingredient = graphene.Field(IngredientType)

    def mutate(self, info, **kwargs):
        form = IngredientForm(kwargs)

        # definir antes ingredient, para que el caso de que ok sea False, 
        # ingredient tenga un valor definido
        ingredient = None
        ok = form.is_valid()
        if ok:
            ingredient = form.save()

        return CreateIngredientMutation(
            ok=ok,
            errors=form.errors or None,
            ingredient=ingredient,
        )


class DeleteIngredientMutation(graphene.Mutation):
    class Arguments:
        ingredientId = graphene.ID()

    ok = graphene.Boolean()
    errors = AnyType()
    ingredient = graphene.Field(IngredientType)
    ingredient_name = graphene.String()

    def mutate(self, info, **kwargs):
        ingredient = Ingredient.objects.get(id=kwargs['ingredientId'])
        ingredient_name = ingredient.name

        if ingredient:
            print("exists!")
            ok = True
            errors = None
            ingredient.delete()
        else:
            ok = False
            errors = "Error"


        return DeleteIngredientMutation(
            ok=ok,
            errors=errors,
            ingredient_name=ingredient_name
        )

class Mutation(object):
    create_ingredient = CreateIngredientMutation.Field()
    delete_ingredient = DeleteIngredientMutation.Field()
