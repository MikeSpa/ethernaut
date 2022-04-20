from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import GatekeeperOne, AttackGatekeeperOne, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_GatekeeperOne():
    account = get_account()
    gatekeeper = GatekeeperOne.deploy(
        {"from": account},
    )
    return gatekeeper


def deploy_AttackGatekeeperOne(victim):
    account = get_account()
    attack = AttackGatekeeperOne.deploy(
        victim,
        {"from": account},
    )
    return attack


def main():
    print(network.show_active())
    account = get_account()

    gatekeeper = deploy_GatekeeperOne()
    # gatekeeper_address = "0x8Cfa32c255B90d51acB6bc0898736E768b0e178D"
    # gatekeeper = Contract.from_abi(
    #     GatekeeperOne._name, gatekeeper_address, GatekeeperOne.abi
    # )

    attack = deploy_AttackGatekeeperOne(gatekeeper)
    # attack = AttackGatekeeperOne[-1]

    print(f"Entrant? : {gatekeeper.entrant()}")

    attack.attack(
        {
            "from": account,
        }
    )
    print(f"Entrant? : {gatekeeper.entrant()}")
