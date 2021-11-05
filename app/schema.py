import graphene
from app.api.stats.queries import Query as StatsQuery


class Query(StatsQuery, graphene.ObjectType):
    """
    This class will inherit from multiple Queries
    as we begin to add more apps to our project
    """
    pass


class Mutation(graphene.ObjectType):
    """
    This class will inherit from multiple Mutations
    as we begin to add more apps to our project
    """
    pass


schema = graphene.Schema(query=Query)
