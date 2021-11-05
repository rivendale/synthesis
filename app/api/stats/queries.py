import graphene
from django.db.models import Q
from graphene_django.types import ObjectType

from ..helpers.pagination_helper import pagination_helper
from ..helpers.validate_address import validate_address
from .models import AddressTokens
from .object_types import StatsaginatedType, StatsType


class Query(ObjectType):
    address = graphene.Field(StatsType, address=graphene.String())
    addresses = graphene.Field(StatsaginatedType,
                               search=graphene.String(),
                               page=graphene.Int(),
                               limit=graphene.Int())

    def resolve_address(self, info, **kwargs):
        address = kwargs.get('address', None)
        return validate_address(address)

    def addresses(self, info, search=None, **kwargs):
        """
        Query to fetch all addresses
        """
        try:
            page = int(kwargs.get('page'))
            limit = int(kwargs.get('limit'))
        except Exception:
            page = 1
            limit = 10

        if search:
            filter = (
                Q(address__icontains=search)
            )
            addresses = AddressTokens.objects.filter(filter).all()
        else:
            addresses = AddressTokens.objects.all()
        return pagination_helper(addresses, page, limit, StatsaginatedType)
