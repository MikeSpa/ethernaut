from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Denial, AttackDenial, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_Denial():
    acc1 = get_account(index=1)
    denial = Denial.deploy(
        {"from": acc1},
    )
    return denial


def deploy_AttackDenial(denial):
    account = get_account()
    attack_contract = AttackDenial.deploy(
        denial,
        {"from": account},
    )
    return attack_contract


def main():
    print(network.show_active())
    account = get_account()
    # acc1 = get_account(index=1)

    # denial = deploy_Denial()
    denial_address = "0x13b3edB7C0a877Fd6A0E6d511b1C585F9cF5faba"
    denial = Contract.from_abi(Denial._name, denial_address, Denial.abi)

    attack_contract = deploy_AttackDenial(denial)

    # denial.withdraw({"from": acc1})
