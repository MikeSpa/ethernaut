from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import GatekeeperTwo, AttackGatekeeperTwo, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_GatekeeperTwo():
    account = get_account()
    gatekeeper = GatekeeperTwo.deploy(
        {"from": account},
    )
    return gatekeeper


def deploy_AttackGatekeeperTwo(victim):
    account = get_account()
    attack = AttackGatekeeperTwo.deploy(
        victim,
        {"from": account},
    )
    return attack


def main():
    print(network.show_active())
    account = get_account()

    # gatekeeper = deploy_GatekeeperTwo()
    gatekeeper_address = "0xe735cf658374d1fEB46363c3871629f016FFeb8F"
    gatekeeper = Contract.from_abi(
        GatekeeperTwo._name, gatekeeper_address, GatekeeperTwo.abi
    )

    attack = deploy_AttackGatekeeperTwo(gatekeeper)
    # attack = AttackGatekeeperTwo[-1]

    print(f"Entrant? : {gatekeeper.entrant()}")

    # attack.attack({"from": account})
    print(f"Entrant? : {gatekeeper.entrant()}")
