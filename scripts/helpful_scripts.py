from brownie import (
    network,
    accounts,
    config,
)
from web3 import Web3

FORKED_LOCAL_ENVIRNOMENT = ["mainnet-fork", "mainnet-fork2"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "hardhat"]

CENT = Web3.toWei(100, "ether")
POINT_ONE = Web3.toWei(0.1, "ether")
TEN = Web3.toWei(10, "ether")
ONE = Web3.toWei(1, "ether")

DECIMALS = 18


def get_account(index=None, id=None, user=None):
    if user == 1:
        accounts.add(config["wallets"]["from_key_user"])
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRNOMENT
    ):
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def get_verify_status():
    verify = (
        config["networks"][network.show_active()]["verify"]
        if config["networks"][network.show_active()].get("verify")
        else False
    )
    return verify


def main():
    pass
