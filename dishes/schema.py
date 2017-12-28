import graphene
from graphene_django import DjangoObjectType

from .models import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    category = graphene.Field(lambda: CategoryType)

    def mutate(self, info, name, description=""):
        print(info.operation)
        if name:
            new_category = Category.objects.create(name=name, description=description)
        else:
            ok = False
            return CreateCategory(category=None, ok=ok)
        category = CategoryType(name=name, description=description)
        ok = True
        return CreateCategory(category=category, ok=ok)


class EditCategory(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        name = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    category = graphene.Field(lambda: CategoryType)

    def mutate(self, info, id, name=None, description=None):
        if id:
            cat = Category.objects.get(id=id)
            if name:
                cat.name = name
            if description:
                cat.description = description
            cat.save()
            category = CategoryType(id=cat.pk, name=cat.name, description=cat.description)
            ok = True
            return EditCategory(category=category, ok=ok)
        else:
            ok = False
            return EditCategory(category=None, ok=ok)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    category = graphene.Field(lambda: CategoryType)

    def mutate(self, info, id):
        if id:
            cat = Category.objects.get(id=id)
            cat.delete()
            category = CategoryType(name=cat.name, description=cat.description)
            ok = True
            return DeleteCategory(category=category, ok=ok)
        else:
            ok = False
            return DeleteCategory(category=None, ok=ok)


class Query:
    all_categories = graphene.List(CategoryType)

    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)
