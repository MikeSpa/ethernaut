from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from web3 import Web3
from web3.auto import w3
from brownie import (
    PuzzleWalletFactory,
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


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    # deployer = get_account(index=1)  # local testing
    print(f"account address: {account}")
    # print(f"deployer address: {deployer}")  # local testing

    # Proxy
    # proxy = deploy_PuzzleWallet()  # local testing
    proxy_address = "0x61D1bB51EB0173E114D1ad0A9f95D41c6073D55e"
    proxy = Contract.from_abi(PuzzleProxy._name, proxy_address, PuzzleProxy.abi)

    print(f"Proxy address: {proxy_address}")

    print(f"Proxy admin: {proxy.admin()}")

    # Proxy contract
    instance = Contract.from_abi(PuzzleWallet._name, proxy_address, PuzzleWallet.abi)

    ### Propose new admin
    print("\n\n### Changing pendingAdmin and owner")
    print(f"Proxy pending admin: {proxy.pendingAdmin()}")
    print(f"owner: {instance.owner()}")
    proxy.proposeNewAdmin(account, {"from": account})
    print(f"Proxy pending admin: {proxy.pendingAdmin()}")
    print(f"New owner: {instance.owner()}")

    ### Get ourselves whitelisted
    print("\n\n### Getting whitlisted")
    print(f"Account whitelisted?: {instance.whitelisted(account)}")
    instance.addToWhitelist(account, {"from": account})
    print(f"Account whitelisted?: {instance.whitelisted(account)}")

    ### Reduce balance to zero
    print("\n\n### Increasing our balance with multicall")
    wallet_balance = instance.balance()
    print(f"Wallet Balance: {wallet_balance}")
    print(f"Account Balance on wallet: {instance.balances(account)}")

    ### create multicall calldata:
    # need two call first a deposit then a multicall with deposit

    # method id for the first deposit() call
    deposit_hash = Web3.keccak(text="deposit()")[:4].hex()
    # here we encode the calldata to call multicall with one argument, the deposit() call
    multicall_deposit_calldata = instance.multicall.encode_input([deposit_hash])
    # we can now packed those two calldata together to have the final argument to give to multicall
    data = [deposit_hash, multicall_deposit_calldata]

    ### multicall call
    print(f"\nMulticall calldata: {data}")
    instance.multicall(data, {"from": account, "value": wallet_balance})
    print(f"Wallet Balance: {instance.balance()}")
    print(f"Account Balance on wallet: {instance.balances(account)}")

    ### empty the balance
    print("\n\n### Emptying the balance with execute")
    instance.execute(
        account,
        instance.balances(account),
        Web3.keccak(text="transfer(int)")[:4].hex(),
        {"from": account},
    )

    print(f"Wallet Balance: {instance.balance()}")
    print(f"Account Balance on wallet: {instance.balances(account)}")

    ### Setting new max balance and new admin
    print("\n\n### Changing max balance and admin")
    print(f"Max Balance: {instance.maxBalance()}")
    print(f"Wallet admin: {proxy.admin()}")
    instance.setMaxBalance(account.address, {"from": account})
    print(f"Max Balance: {instance.maxBalance()}")
    print(f"Wallet admin: {proxy.admin()}")
