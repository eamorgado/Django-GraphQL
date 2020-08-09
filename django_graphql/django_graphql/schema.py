import graphene
import movies.schema as sch

class Query(sch.Query, graphene.ObjectType):#Class will inherit from sch.Query
    pass

class Mutation(sch.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)