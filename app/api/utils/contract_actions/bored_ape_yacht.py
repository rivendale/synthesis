
from .contract_instance import get_contract_instance


def get_bayc_address_token_count(address):
    """
    Get the number of tokens owned by an address
    """
    contract = get_contract_instance('bayc')
    return contract.functions.balanceOf(address).call()
