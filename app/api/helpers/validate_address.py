from django.conf import settings
from graphql import GraphQLError
from web3 import Web3

from ..stats.models import AddressTokens
from ..utils.contract_actions.bored_ape_yacht import \
    get_bayc_address_token_count
from ..utils.contract_actions.rumble_kong_league import \
    get_rkl_address_token_count
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
        provider.toChecksumAddress(address)
        obj = AddressTokens.objects.get(address=address)
    except Exception as e:
        if isinstance(e, ValueError):
            raise GraphQLError(error_dict['invalid_input'].format('ethereum address'))
        if isinstance(e, AddressTokens.DoesNotExist):
            rumble_kong_league_token_count = get_rkl_address_token_count(address)
            bored_ape_yacht_token_count = get_bayc_address_token_count(address)
            data = {
                'address': address,
                'bored_ape_yacht_token_count': bored_ape_yacht_token_count,
                'rumble_kong_league_token_count': rumble_kong_league_token_count
            }

            obj = AddressTokens.objects.create(**data)

    return obj
