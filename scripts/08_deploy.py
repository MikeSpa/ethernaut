from scripts.helpful_scripts import get_account, ONE
from brownie import Vault, network, Contract, interface
from web3 import Web3
from web3.auto import w3


def deploy_Vault(password):
    owner = get_account(index=1)
    vault = Vault.deploy(
        password,
        {"from": owner},
    )
    return vault


def main():
    print("test")
    print(network.show_active())
    account = get_account()
    # password = "53cr31pa55w0rd".encode("utf-8")  # local test
    # vault = deploy_Vault(password.hex())  # local test
    vault_address = "0x12f6EDd889480b0d49503Fda0618c600710b8aC3"
    vault = Contract.from_abi(Vault._name, vault_address, Vault.abi)
    print(vault.locked())
    p = w3.eth.get_storage_at(vault.address, 1)
    print(p)
    vault.unlock(p, {"from": account})
    print(vault.locked())
