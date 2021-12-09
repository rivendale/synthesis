
from .contract_instance import get_contract_instance
from .contract_actions import (get_token_ids, get_token_uri)


def get_rkl_address_token_count(address):
    """
    Get the number of tokens owned by an address
    """
    contract = get_contract_instance('rkl')

    balance = 0
    try:
        balance = contract.functions.balanceOf(address).call()
    except Exception as e:
        print(e)
    return balance


def get_rkl_tokens(address) -> list:
    contract = get_contract_instance('rkl')
    token_ids = get_token_ids(address, contract)
    tokens = []
    for token_id in token_ids:
        token = get_token_uri(token_id, contract)
        if token:
            token['token_id'] = token_id
            tokens.append(token)
    return tokens
