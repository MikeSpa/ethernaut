from brownie import (
    network,
    accounts,
    config,
    interface,
    # MockV3Aggregator,
    # Contract,
    # MockWETH,
    # MockDAI,
    # MockLendingPool,
    # MockERC20,
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


# def get_weth(amount=0.1):
#     print(f"#get_weth, amt={amount}")
#     account = get_account()
#     weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
#     deposit_tx = weth.deposit({"from": account, "value": amount * 10 ** 18})
#     deposit_tx.wait(1)
#     print(f"Received {amount} WETH")
#     return deposit_tx


# def get_eth(amount=0.1):
#     print(f"#get_eth, amt={amount}")
#     account = get_account()
#     weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
#     withdraw_tx = weth.withdraw(amount * 10 ** 18, {"from": account})
#     withdraw_tx.wait(1)
#     print(f"Received {amount} ETH")
#     return withdraw_tx


# def approve_erc20(token_address, spender, amount, account):
#     print(f"#approve_erc20, {amount} {token_address} for {spender}")
#     erc20 = interface.IERC20(token_address)
#     tx = erc20.approve(spender, amount, {"from": account})
#     tx.wait(1)
#     print("Approved")


# def get_asset_price(price_feed_address):
#     price_feed = interface.AggregatorV3Interface(price_feed_address)
#     latest_price = price_feed.latestRoundData()[1]
#     converted_latest_price = Web3.fromWei(latest_price, "ether")
#     print(f"The price is {converted_latest_price}")
#     return float(converted_latest_price)


# contract_to_mock = {
#     "dai_eth_price_feed": MockV3Aggregator,
#     "weth_token": MockWETH,
#     "eth_usd_price_feed": MockV3Aggregator,
#     "dai_usd_price_feed": MockV3Aggregator,
#     "fau_token": MockDAI,
#     "lending_pool": MockLendingPool,
#     "compound_lending": MockLendingPool,
#     "aWETH": MockERC20,
#     "DAI": MockDAI,
#     "cDAI": MockERC20,
# }


# def get_contract(contract_name):
#     """
#     This script will either:
#             - Get an address from the config
#             - Or deploy a mock to use for a network that doesn't have it
#         Args:
#             contract_name (string): This is the name that is refered to in the
#             brownie config and 'contract_to_mock' variable.
#         Returns:
#             brownie.network.contract.ProjectContract: The most recently deployed
#             Contract of the type specificed by the dictonary. This could be either
#             a mock or the 'real' contract on a live network.
#     """
#     contract_type = contract_to_mock[contract_name]
#     if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
#         if len(contract_type) <= 0:
#             deploy_mocks()
#         contract = contract_type[-1]

#     else:
#         try:
#             contract_address = config["networks"][network.show_active()][contract_name]
#             contract = Contract.from_abi(
#                 contract_type._name, contract_address, contract_type.abi
#             )
#         except KeyError:
#             print(
#                 f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
#             )
#     return contract


# def deploy_mocks():
#     account = get_account()
#     print(f"### The active netwok is {network.show_active()}")
#     print("### Deploying Mocks...")
#     mock_price_feed = MockV3Aggregator.deploy(
#         DECIMALS, INITIAL_PRICE_FEED_VALUE, {"from": account}
#     )
#     print(f"MockV3Aggregator deployed to {mock_price_feed}")

#     mock_weth_token = MockWETH.deploy({"from": account})
#     print(f"MockWETH deployed to {mock_weth_token.address}")
#     mock_dai_token = MockDAI.deploy({"from": account})
#     print(f"MockDAI deployed to {mock_dai_token.address}")

#     mock_lending_pool = MockLendingPool.deploy({"from": account})
#     print(f"MockLendingPool deployed to {mock_lending_pool}")


# def get_verify_status():
#     verify = (
#         config["networks"][network.show_active()]["verify"]
#         if config["networks"][network.show_active()].get("verify")
#         else False
#     )
#     return verify


def main():
    pass
