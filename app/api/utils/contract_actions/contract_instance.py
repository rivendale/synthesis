from web3 import Web3
from django.conf import settings
import os

provider = Web3(Web3.HTTPProvider(settings.RPC_URL))

CONTRACTS = {
    'bayc': {
        'abi': "bayc.json",
        'address': settings.BAYC_CONTRACT_ADDRESS,
    },
    'rkl': {
        'abi': "rkl.json",
        'address': settings.RKL_CONTRACT_ADDRESS,
    }
}


def get_contract_instance(contract_name):
    '''
    Returns the contract instance for the given contract name
    '''
    contract_details = CONTRACTS.get(contract_name, "bayc")
    abi_path = os.path.join(
        settings.BASE_DIR,
        f"api/utils/contract_abis/{contract_details['abi']}")
    abi = open(abi_path, 'r').read()
    contract = provider.eth.contract(
        address=contract_details['address'],
        abi=abi)
    return contract
