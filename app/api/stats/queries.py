import graphene
from django.conf import settings
from django.db.models import Count, Q
from graphene_django.types import ObjectType
from graphql import GraphQLError
from web3 import Web3

from ..helpers.pagination_helper import pagination_helper
from ..helpers.validate_address import (update_bayc_address_nfts,
                                        update_rkl_address_nfts,
                                        validate_address)
from ..helpers.validation_errors import error_dict
from .models import AddressTokens, BaycToken, RklToken
from .object_types import (BaycpaginatedType, RklpaginatedType,
                           StatspaginatedType, StatsType)

provider = Web3(Web3.HTTPProvider(settings.RPC_URL))


class Query(ObjectType):
    address = graphene.Field(StatsType, address=graphene.String())
    addresses = graphene.Field(StatspaginatedType,
                               address=graphene.String(),
                               page=graphene.Int(),
                               limit=graphene.Int())

    bayc_tokens = graphene.Field(BaycpaginatedType,
                                 address=graphene.String(),
                                 page=graphene.Int(),
                                 limit=graphene.Int())
    rkl_tokens = graphene.Field(RklpaginatedType,
                                address=graphene.String(),
                                page=graphene.Int(),
                                limit=graphene.Int())

    def resolve_rkl_tokens(self, info, address=None, **kwargs):
        """
        Query to fetch all rkl tokens
        """
        try:
            page = int(kwargs.get('page'))
            limit = int(kwargs.get('limit'))
        except Exception:
            page = 1
            limit = 10
        if address:
            try:
                provider.toChecksumAddress(address)
                tokens = RklToken.objects.filter(
                    rumble_kong_league__address__icontains=address).all()
            except Exception as e:
                if isinstance(e, ValueError):
                    raise GraphQLError(
                        error_dict['invalid_input'].format('ethereum address'))
        else:
            tokens = RklToken.objects.all()
        tokens = tokens.order_by('-created_at')
        return pagination_helper(tokens, page, limit, RklpaginatedType)

    def resolve_bayc_tokens(self, info, address=None, **kwargs):
        """
        Query to fetch all bayc tokens
        """
        try:
            page = int(kwargs.get('page'))
            limit = int(kwargs.get('limit'))
        except Exception:
            page = 1
            limit = 10
        if address:
            try:
                provider.toChecksumAddress(address)
                tokens = BaycToken.objects.filter(
                    bored_ape_yacht__address__icontains=address).all()
            except Exception as e:
                if isinstance(e, ValueError):
                    raise GraphQLError(
                        error_dict['invalid_input'].format('ethereum address'))
        else:
            tokens = BaycToken.objects.all()
        tokens = tokens.order_by('-created_at')
        return pagination_helper(tokens, page, limit, BaycpaginatedType)

    def resolve_address(self, info, **kwargs):
        address = kwargs.get('address', None)
        return validate_address(address)

    def resolve_addresses(self, info, address=None, **kwargs):
        """
        Query to fetch all addresses
        """
        try:
            page = int(kwargs.get('page'))
            limit = int(kwargs.get('limit'))
        except Exception:
            page = 1
            limit = 10

        if address:
            try:
                provider.toChecksumAddress(address)
                AddressTokens.objects.get(address=address)
            except Exception as e:
                if isinstance(e, ValueError):
                    raise GraphQLError(
                        error_dict['invalid_input'].format('ethereum address'))
                if isinstance(e, AddressTokens.DoesNotExist):
                    obj = AddressTokens.objects.create(**{"address": address,
                                                          'fetching_stats': True})
                    update_bayc_address_nfts.delay(obj.id)
                    update_rkl_address_nfts.delay(obj.id)
            filter = (
                Q(address__icontains=address)
            )
            addresses = AddressTokens.objects.filter(filter).all()

        else:
            addresses = AddressTokens.objects.all()
        addresses = (addresses.annotate(bayc_count=Count('bored_ape_yacht'),
                                        rkl_count=Count('rumble_kong_league'))
                     .order_by('-bayc_count', '-rkl_count'))
        return pagination_helper(addresses, page, limit, StatspaginatedType)
