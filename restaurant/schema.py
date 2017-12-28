import graphene
import dishes.schema


class Query(dishes.schema.Query, graphene.ObjectType):
    pass


class Mutations(graphene.ObjectType):
    create_category = dishes.schema.CreateCategory.Field()
    edit_category = dishes.schema.EditCategory.Field()
    delete_category = dishes.schema.DeleteCategory.Field()
    create_dish = dishes.schema.CreateDish.Field()
    edit_dish = dishes.schema.EditDish.Field()
    delete_dish = dishes.schema.DeleteDish.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
