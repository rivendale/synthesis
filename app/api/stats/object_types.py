import graphene
from graphene_django.types import DjangoObjectType

from .models import AddressTokens


class StatsType(DjangoObjectType):
    """
    Create a GraphQL type for the address stats model
    """

    class Meta:
        '''Defines the fields to be serialized in the address stats model'''
        model = AddressTokens


class StatsaginatedType(graphene.ObjectType):
    """
    Question pagination input types
    """
    count = graphene.Int()
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    items = graphene.List(StatsType)
