# 26) DoubleEntryPoint

Success condition:
> This level features a CryptoVault with special functionality, the sweepToken function. This is a common function to retrieve tokens stuck in a contract. The CryptoVault operates with an underlying token that can't be swept, being it an important core's logic component of the CryptoVault, any other token can be swept.  
The underlying token is an instance of the DET token implemented in DoubleEntryPoint contract definition and the CryptoVault holds 100 units of it. Additionally the CryptoVault also holds 100 of LegacyToken LGT.  
In this level you should figure out where the bug is in CryptoVault and protect it from being drained out of tokens.  
The contract features a Forta contract where any user can register its own detection bot contract. Forta is a decentralized, community-based monitoring network to detect threats and anomalies on DeFi, NFT, governance, bridges and other Web3 systems as quickly as possible. Your job is to implement a detection bot and register it in the Forta contract. The bot's implementation will need to raise correct alerts to prevent potential attacks or bug exploits.

There is two steps in this level, first we must find a vulnerability to sweep the DET form the vault, and second we need to deploy a forta detection bot to detect a transaction which uses this vulnerability.

## The vunerability

If we try to directly sweep the token with the `sweepToken()` function:
```solidity
function sweepToken(IERC20 token) public {
    require(token != underlying, "Can't transfer underlying token");
    token.transfer(sweptTokensRecipient, token.balanceOf(address(this)));
}
```
It will revert since the DET is the underlying token. But if we call `sweepToken()` with the legacy token as argument, we will arrive at the second line which will call:
```solidity
function transfer(address to, uint256 value)
    public
    override
    returns (bool)
{
    if (address(delegate) == address(0)) {
        return super.transfer(to, value);
    } else {
        return delegate.delegateTransfer(to, value, msg.sender);
    }
}
```
This in turn will call:
```solidity
function delegateTransfer(
    address to,
    uint256 value,
    address origSender
) public override onlyDelegateFrom fortaNotify returns (bool) {
    _transfer(origSender, to, value);
    return true;
}
```
which will transfer the DET to our account. 

## The Bot

But we can see that one of the modifier is `fortaNotify`:
```solidity
modifier fortaNotify() {
        address detectionBot = address(forta.usersDetectionBots(player));

        // Cache old number of bot alerts
        uint256 previousValue = forta.botRaisedAlerts(detectionBot);

        // Notify Forta
        forta.notify(player, msg.data);

        // Continue execution
        _;

        // Check if alarms have been raised
        if (forta.botRaisedAlerts(detectionBot) > previousValue)
            revert("Alert has been triggered, reverting");
    }
```
This will check how many alerts have been raised by a given bot, notify the bot of a coming call, run the `delegateTransfer()` function and after that, check to see if an alert was raised during the `delegateTransfer()` function. If its the case, it will revert the transaction.

`forta.notify()`:
```solidity
function notify(address user, bytes calldata msgData) external override {
    if (address(usersDetectionBots[user]) == address(0)) return;
    try usersDetectionBots[user].handleTransaction(user, msgData) {
        return;
    } catch {}
}
```
will actually call our bot using a `handleTransaction()` function and passing it the msg.data of `delegateTransfer()`. Since the exploit appear when we try to use the `delegateTransfer()` function, we can simply check the [function signature of msgData](https://ethereum.stackexchange.com/questions/61826/how-to-extract-function-signature-from-msg-data) to see if its `delegateTransfer()` and raise an alert if its the case. 
  




---
### Double Entry Point Token
[TrueUSD ↔ Compound Vulnerability](https://medium.com/chainsecurity/trueusd-compound-vulnerability-bc5b696d29e2)  
[Balancer](https://forum.balancer.fi/t/medium-severity-bug-found/3161)  

### Misc
[Forta](https://docs.forta.network/en/latest/)  
[Extract signature from msg.data](https://ethereum.stackexchange.com/questions/61826/how-to-extract-function-signature-from-msg-data)


---
## Level completed!

Congratulations!

This is the first experience you have with a Forta bot.

Forta comprises a decentralized network of independent node operators who scan all transactions and block-by-block state changes for outlier transactions and threats. When an issue is detected, node operators send alerts to subscribers of potential risks, which enables them to take action.

The presented example is just for educational purpose since Forta bot is not modeled into smart contracts. In Forta, a bot is a code script to detect specific conditions or events, but when an alert is emitted it does not trigger automatic actions - at least not yet. In this level, the bot's alert effectively trigger a revert in the transaction, deviating from the intended Forta's bot design.

Detection bots heavily depends on contract's final implementations and some might be upgradeable and break bot's integrations, but to mitigate that you can even create a specific bot to look for contract upgrades and react to it. Learn how to do it here.

You have also passed through a recent security issue that has been uncovered during OpenZeppelin's latest [collaboration with Compound protocol](https://compound.finance/governance/proposals/76).

Having tokens that present a double entry point is a non-trivial pattern that might affect many protocols. This is because it is commonly assumed to have one contract per token. But it was not the case this time :) You can read the entire details of what happened [here](https://blog.openzeppelin.com/compound-tusd-integration-issue-retrospective/).

