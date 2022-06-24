from scripts.helpful_scripts import get_account
from web3 import Web3
from web3.auto import w3
from brownie import (
    DoubleEntryPoint,
    Forta,
    CryptoVault,
    LegacyToken,
    DoubleEntryPointFactory,
    DetectionBot,
    network,
    Contract,
)


def deploy_DoubleEntryPointFactory():
    account = get_account()
    deployer = get_account(index=1)
    factory = DoubleEntryPointFactory.deploy(
        {"from": deployer},
    )
    tx = factory.createInstance(account, {"from": deployer})
    proxy = tx.return_value
    return proxy, factory


def deploy_DetectionBot(forta):
    account = get_account()
    attack = DetectionBot.deploy(forta, {"from": account})
    return attack


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    # (
    #     double_entry_point_address,
    #     factory,
    # ) = deploy_DoubleEntryPointFactory()  # local testing
    double_entry_point_address = "0x9C8E7742bc764fB6EEB8191F44018cf63A7dDca4"

    double_entry_point = Contract.from_abi(
        DoubleEntryPoint._name, double_entry_point_address, DoubleEntryPoint.abi
    )
    legacy_token = Contract.from_abi(
        LegacyToken._name, double_entry_point.delegatedFrom(), LegacyToken.abi
    )
    forta = Contract.from_abi(Forta._name, double_entry_point.forta(), Forta.abi)
    vault = Contract.from_abi(
        CryptoVault._name, double_entry_point.cryptoVault(), CryptoVault.abi
    )

    # Deploy bot
    bot = deploy_DetectionBot(forta)
    # register bot with forta
    forta.setDetectionBot(bot, {"from": account})

    # try to sweep underlying token, should raise alert
    # print(f"DET balance: {double_entry_point.balanceOf(account)}")  # local testing
    # vault.sweepToken(legacy_token, {"from": account}) # local testing, should revert because of alert
    # print(f"DET balance: {double_entry_point.balanceOf(account)}")  # local testing
