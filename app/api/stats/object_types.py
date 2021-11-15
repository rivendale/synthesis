import graphene
from graphene.types.generic import GenericScalar
from graphene_django.types import DjangoObjectType

from .models import AddressTokens, RklToken, BaycToken


class RklTokenType(DjangoObjectType):
    """
    Create a GraphQL type for the address RklToken model
    """
    metadata = GenericScalar()

    class Meta:
        '''Defines the fields to be serialized in the address RklToken model'''
        model = RklToken


class BaycTokenType(DjangoObjectType):
    """
    Create a GraphQL type for the address BaycToken model
    """
    metadata = GenericScalar()

    class Meta:
        '''Defines the fields to be serialized in the address BaycToken model'''
        model = BaycToken


class StatsType(DjangoObjectType):
    """
    Create a GraphQL type for the address stats model
    """
    bored_ape_yacht_token_count = graphene.Int()
    rumble_kong_league_token_count = graphene.Int()

    def resolve_bored_ape_yacht_token_count(self, *args):
        return self.bored_ape_yacht_token_count

    def resolve_rumble_kong_league_token_count(self, *args):
        return self.rumble_kong_league_token_count

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
