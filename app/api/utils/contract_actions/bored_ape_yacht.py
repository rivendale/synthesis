from .contract_instance import get_contract_instance
from .contract_actions import (get_token_ids, get_token_uri)


def get_bayc_address_token_count(address):
    """
    Get the number of tokens owned by an address
    """
    contract = get_contract_instance('bayc')
    # rkl_contract = get_contract_instance('rkl')
    # for i in range(1, 60):
    #     add = contract.functions.ownerOf(i).call()
    #     bal = contract.functions.balanceOf(add).call()
    #     rkl_bal = rkl_contract.functions.balanceOf(add).call()
    #     if rkl_bal > 0:
    #         print({add: {"bayc": bal, "rkl": rkl_bal}})
    # breakpoint()
    balance = 0
    try:
        balance = contract.functions.balanceOf(address).call()
    except Exception as e:
        print(e)
    return balance


def get_bayc_tokens(address) -> list:
    contract = get_contract_instance('bayc')
    token_ids = get_token_ids(address, contract)
    tokens = []
    for token_id in token_ids:
        token = get_token_uri(token_id, contract)
        if token:
            token['token_id'] = token_id
            tokens.append(token)
    return tokens
