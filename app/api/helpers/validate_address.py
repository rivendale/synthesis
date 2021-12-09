from django.conf import settings
from django.db import transaction
from graphql import GraphQLError
from web3 import Web3
from app import celery_app

from ..stats.models import AddressTokens, BaycToken, RklToken
from ..utils.contract_actions.bored_ape_yacht import (
    get_bayc_tokens, get_bayc_address_token_count)
from ..utils.contract_actions.rumble_kong_league import (
    get_rkl_tokens, get_rkl_address_token_count)
from .validation_errors import error_dict

provider = Web3(Web3.HTTPProvider(settings.RPC_URL))


def validate_address(address):
    '''
    Checks if an object that address is valid.
    Args:
        address (str): address
    Raise:
        raise GraphQLError if the address is invalid
    Return:
        obj (obj): model object
    '''
    if not address:
        raise GraphQLError(error_dict['empty_field'].format('address field'))
    try:
        address = provider.toChecksumAddress(address.lower())
        obj = AddressTokens.objects.get(address=address)
    except Exception as e:
        if isinstance(e, ValueError):
            raise GraphQLError(error_dict['invalid_input'].format('ethereum address'))
        if isinstance(e, AddressTokens.DoesNotExist):
            bayc_tokens = get_bayc_tokens(address)
            obj = AddressTokens.objects.create(**{"address": address})
            for token in bayc_tokens:
                data = {
                    'token_id': token.pop('token_id'),
                    'metadata': token,
                }
                bayc_obj = BaycToken.objects.create(**data)
                obj.bored_ape_yacht.add(bayc_obj)
            rkl_tokens = get_rkl_tokens(address)
            for token in rkl_tokens:
                data = {
                    'token_id': token.pop('token_id'),
                    'metadata': token,
                }
                rkl_obj = RklToken.objects.create(**data)
                obj.rumble_kong_league.add(rkl_obj)

    return obj


@celery_app.task(name="update rkl address nfts")
def update_rkl_address_nfts(address_id=None):
    '''
    Update the number of NFTs for each address in the Rumble Kong League
    '''
    address_obj = None
    if address_id:
        address_obj = AddressTokens.objects.get(id=address_id)
    addresses = [address_obj] if address_obj else AddressTokens.objects.all()
    for address in addresses:
        addr = Web3.toChecksumAddress(address.address.lower())
        with transaction.atomic():
            if address.bored_ape_yacht_token_count \
                    != get_rkl_address_token_count(addr):
                address.rumble_kong_league.all().delete()
                tokens = get_rkl_tokens(addr)
                for token in tokens:
                    data = {
                        'token_id': token.pop('token_id'),
                        'metadata': token,
                    }
                    rkl_obj = RklToken.objects.create(**data)
                    address.rumble_kong_league.add(rkl_obj)
            address.fetching_stats = False
            address.save()


@celery_app.task(name="update bayc address nfts")
def update_bayc_address_nfts(address_id=None):
    '''
    Update the number of NFTs for each address in the Bored Ape Yacht
    '''
    address_obj = None
    if address_id:
        address_obj = AddressTokens.objects.get(id=address_id)
    addresses = [address_obj] if address_obj else AddressTokens.objects.all()
    for address in addresses:
        addr = Web3.toChecksumAddress(address.address.lower())
        with transaction.atomic():
            if address.bored_ape_yacht_token_count \
                    != get_bayc_address_token_count(addr):
                address.bored_ape_yacht.all().delete()
                tokens = get_bayc_tokens(addr)
                for token in tokens:
                    data = {
                        'token_id': token.pop('token_id'),
                        'metadata': token,
                    }
                    bayc_obj = BaycToken.objects.create(**data)
                    address.bored_ape_yacht.add(bayc_obj)
            if address_id:
                update_rkl_address_nfts.delay(address_id)
