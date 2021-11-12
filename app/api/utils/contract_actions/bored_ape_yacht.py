import requests
from django.conf import settings

from .contract_instance import get_contract_instance


def get_bayc_address_token_count(address):
    """
    Get the number of tokens owned by an address
    """
    contract = get_contract_instance('bayc')
    return contract.functions.balanceOf(address).call()


def strip_ipfs_uri_prefix(cid_or_uri):
    if cid_or_uri.startswith('ipfs://'):
        return cid_or_uri.replace("ipfs://", "", 1)

    return cid_or_uri


def make_gateway_url(ipfs_uri, metadata=True):
    url = settings.IPFS_GATEWAY_URL + '/' + strip_ipfs_uri_prefix(ipfs_uri)
    if metadata:
        try:
            metadata = requests.get(url).json()
            metadata['token_url'] = url
            metadata['ipfs_uri'] = ipfs_uri
            metadata['image_url'] = settings.IPFS_GATEWAY_URL + \
                '/' + strip_ipfs_uri_prefix(metadata['image'])
        except Exception as e:
            print(e)
        return metadata
    return url


def get_token_uri(token_id, get_uri=True) -> str:
    contract = get_contract_instance('bayc')
    token = contract.functions.tokenURI(token_id).call()
    if token and get_uri:
        token = make_gateway_url(token)
    return token


def get_token_ids(address) -> list:
    contract = get_contract_instance('bayc')
    balance = contract.functions.balanceOf(address).call()
    token_ids = []
    for i in range(balance):
        id = contract.functions.tokenOfOwnerByIndex(address, i).call()
        token_ids.append(id)
    return token_ids


def get_bayc_tokens(address) -> list:
    token_ids = get_token_ids(address)
    tokens = []
    for token_id in token_ids:
        token = get_token_uri(token_id)
        if token:
            token['token_id'] = token_id
            tokens.append(token)
    return tokens
