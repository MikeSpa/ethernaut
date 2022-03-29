from scripts.helpful_scripts import POINT_ONE, get_account, ONE
from brownie import AttackKing, network


def deploy_AttackKing(king):
    account = get_account()
    attack_king = AttackKing.deploy(
        king,
        {"from": account, "value": POINT_ONE / 10},
    )
    return attack_king


def main():
    print(network.show_active())

    king = "0xad98142eF1a1aC2D7541F0d9c57f3ba20E1979aC"
    deploy_AttackKing(king)
