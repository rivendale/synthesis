import requests
from django.conf import settings


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


def get_token_uri(token_id, contract, get_uri=True) -> str:
    token = contract.functions.tokenURI(token_id).call()
    if token and get_uri:
        token = make_gateway_url(token)
    return token


def get_token_ids(address, contract) -> list:
    balance = contract.functions.balanceOf(address).call()
    token_ids = []
    for i in range(balance):
        id = contract.functions.tokenOfOwnerByIndex(address, i).call()
        token_ids.append(id)
    return token_ids
