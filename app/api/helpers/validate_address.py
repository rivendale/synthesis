from django.db import transaction
from graphql import GraphQLError
from app import celery_app

from ..stats.models import AddressTokens, BaycToken
from ..utils.contract_actions.bored_ape_yacht import (
    get_bayc_tokens, get_bayc_address_token_count)
from .validation_errors import error_dict

from .validation_errors import error_dict
from ..stats.models import AddressTokens


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
        obj = AddressTokens.objects.get(address=address)
    except Exception as e:
        if isinstance(e, ValueError):
            raise GraphQLError(error_dict['invalid_input'].format('ethereum address'))
        if isinstance(e, AddressTokens.DoesNotExist):
            tokens = get_bayc_tokens(address)
            obj = AddressTokens.objects.create(**{"address": address})
            for token in tokens:
                data = {
                    'token_id': token.pop('token_id'),
                    'metadata': token,
                }
                bayc_obj = BaycToken.objects.create(**data)
                obj.bored_ape_yacht.add(bayc_obj)

    return obj


@celery_app.task(name="update bayc address nfts")
def update_bayc_address_nfts():
    '''
    Update the number of NFTs for each address in the Bored Ape Yacht
    '''

    for address in AddressTokens.objects.all():
        with transaction.atomic():
            address.bored_ape_yacht.all().delete()
            if address.bored_ape_yacht_token_count \
                    != get_bayc_address_token_count(address.address):
                tokens = get_bayc_tokens(address.address)
                for token in tokens:
                    data = {
                        'token_id': token.pop('token_id'),
                        'metadata': token,
                    }
                    bayc_obj = BaycToken.objects.create(**data)
                    address.bored_ape_yacht.add(bayc_obj)
