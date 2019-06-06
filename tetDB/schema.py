import graphene

import tetDB.employees.schema

class Mutation(tetDB.employees.schema.Mutation, graphene.ObjectType):
    pass

class Query(tetDB.employees.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
