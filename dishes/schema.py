import graphene
from graphene_django import DjangoObjectType

from .models import Category, Dish


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


class DishType(DjangoObjectType):
    class Meta:
        model = Dish


class CreateDish(graphene.Mutation):
    class Arguments:
        category_id = graphene.String()
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()

    ok = graphene.Boolean()
    dish = graphene.Field(lambda: DishType)

    def mutate(self, info, category_id, name, description="", price=0):
        if name and name:
            new_dish = Dish.objects.create(category_id=category_id, name=name, description=description, price=price)
        else:
            ok = False
            return CreateDish(dish=None, ok=ok)
        dish = DishType(name=name, description=description, price=price)
        ok = True
        return CreateDish(dish=dish, ok=ok)


class EditDish(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        category_id = graphene.String()
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()
    ok = graphene.Boolean()
    dish = graphene.Field(lambda: DishType)

    def mutate(self, info, id, category_id=None, name=None, description=None, price=None):
        if id:
            d = Dish.objects.get(id=id)
            if name:
                d.name = name
            if description:
                d.description = description
            if price is not None:
                d.price = price
            if category_id:
                d.category_id = category_id
            d.save()
            dish = DishType(id=d.pk, name=d.name, description=d.description, price=d.price)
            ok = True
            return EditDish(dish=dish, ok=ok)
        else:
            ok = False
            return EditDish(dish=None, ok=ok)


class DeleteDish(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    ok = graphene.Boolean()
    dish = graphene.Field(lambda: DishType)

    def mutate(self, info, id):
        if id:
            d = Dish.objects.get(id=id)
            d.delete()
            di = DishType(name=d.name, description=d.description, price=d.price)
            ok = True
            return DeleteDish(dish=di, ok=ok)
        else:
            ok = False
            return DeleteDish(category=None, ok=ok)


class Query:
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())
    all_dishes = graphene.List(DishType)

    dish = graphene.Field(DishType,
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

    def resolve_all_diches(self, info, **kwargs):
        return Dish.objects.select_related('category').all()

    def resolve_dish(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Dish.objects.get(pk=id)

        if name is not None:
            return Dish.objects.get(name=name)
