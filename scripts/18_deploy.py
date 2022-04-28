from scripts.helpful_scripts import POINT_ONE, TEN, get_account, ONE
from brownie import MagicNum, network, Contract
from web3 import Web3
from web3.auto import w3


def create_solver():
    account = get_account()
    bytecode = "0x600A600C602039600A6020F3602a60005260206000F3"
    # bytecode = "0x600a600c600039600a6000f3604260805260206080f3"
    smth = account.transfer(data=bytecode)
    return smth


def main():
    print(network.show_active())
    account = get_account()

    # first we deploy the contract
    # tx = create_solver()
    # print(tx)

    # then we give its address to MagicNum
    solver_address = "0x483D470657426D3E493cdf7010f4f57486C3B918"

    address_instance = "0x95041D54FCD5ac72640B3317A1094436b4148c5f"  # instance address

    magic_num = Contract.from_abi(MagicNum._name, address_instance, MagicNum.abi)

    magic_num.setSolver(solver_address, {"from": account})
