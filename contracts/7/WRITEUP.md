# 7) Force

Success condition:
> Some contracts will simply not take your money ¯\_(ツ)_/¯

>The goal of this level is to make the balance of the contract greater than zero.

The main way to send ether to a smart contract is by calling a `payable` function. `Force.sol` doesn't have one. There a a few other way to force a smart contract to take our ether. One one them is with `selfdestruc()`.

`selfdestruct()` is a special method that destroy a smart contract and send its ether balance to a given address. If we create a contract with a function that call `selfdestruct()` and with the `Force.sol` instance address as its receiver, send it some eth and then call destruct the contract, you will have sent ether to our target contract.

---
### selfdestruct()
The only way to remove code from the blockchain is when a contract at that address performs the selfdestruct operation. The remaining Ether stored at that address is sent to a designated target and then the storage and code is removed from the state. Removing the contract in theory sounds like a good idea, but it is potentially dangerous, as if someone sends Ether to removed contracts, the Ether is forever lost.

### Force a contract to receive ether
[StackExchange](https://ethereum.stackexchange.com/questions/63987/can-a-contract-with-no-payable-function-have-ether)

---
## Level completed

In solidity, for a contract to be able to receive ether, the fallback function must be marked payable.

However, there is no way to stop an attacker from sending ether to a contract by self destroying. Hence, it is important not to count on the invariant address(this).balance == 0 for any contract logic.