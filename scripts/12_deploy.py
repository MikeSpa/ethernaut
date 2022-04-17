from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import Privacy, network, Contract
from web3 import Web3
from web3.auto import w3


def deploy_Privacy(data):
    account = get_account()
    privacy = Privacy.deploy(
        data,
        {"from": account},
    )
    return privacy


# def deploy_Attack(victim):
#     account = get_account()
#     attack = Buildingg.deploy(
#         victim,
#         {"from": account},
#     )
#     return attack


def main():
    print(network.show_active())
    account = get_account()
    data = "32 bytes of da".encode("utf-8")  # local test
    privacy = deploy_Privacy([data, data, data])

    privacy_address = "0x12f6EDd889480b0d49503Fda0618c600710b8aC3"
    # vault = Contract.from_abi(Vault._name, vault_address, Vault.abi)
    print(f"Lock? : {privacy.locked()}")
    for i in range(6):
        p = w3.eth.get_storage_at(privacy.address, i)
        print(p.hex())
        print(len(p))
        # for byte in p:
        #     print(byte.hex(), end=" ")
        # print("\n")
        # for byte in p[len(p) - 16 :]:
        #     print(byte, end=" ")
        # print("\n")
        # print(p[:2])
    start = max(0, len(p) - 16)
    print(p[start:])
    print(p[start:].hex())
    # print(p[start:].encode("utf-8"))
    privacy.unlock(data, {"from": account})
    print(f"Lock? : {privacy.locked()}")
