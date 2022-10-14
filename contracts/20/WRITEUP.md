# 20) Denial

Success condition:
> This is a simple wallet that drips funds over time. You can withdraw the funds slowly by becoming a withdrawing partner.  
If you can deny the owner from withdrawing funds when they call withdraw() (whilst the contract still has funds, and the transaction is of 1M gas or less) you will win this level.

We need to make sure that the owner cannot receive funds when they call ```withdraw()```. Since we can't block them from calling the function, we will have to find a way to block them from executing the instruction that transfer the funds: ```owner.transfer(amountToSend);```.

In order to do that, we just need to make sure the ```partner.call{value: amountToSend}("");``` uses enough gas that the next line cannot be executed. Since ```call{value: smth}``` will call the ```receive()``` function in a contract, we can create a simple attack contract with a ```receive()``` function. In this function we can do anything we want that will waste all the gas given for the transaction. My contract has an infinite loop with ```owner.transfer(address(this).balance);``` inside. Once the transaction run out of gas, we know that the next instruction ```owner.transfer(amountToSend);``` cannot be executed and the level is completed.

---
### low level call
Since we never know what might happen when we call an external contract with call, always make sure to specify a gas limit for this call.


---
## Level completed!

This level demonstrates that external calls to unknown contracts can still create denial of service attack vectors if a fixed amount of gas is not specified.

If you are using a low level call to continue executing in the event an external call reverts, ensure that you specify a fixed gas stipend. For example call.gas(100000).value().

Typically one should follow the checks-effects-interactions pattern to avoid reentrancy attacks, there can be other circumstances (such as multiple external calls at the end of a function) where issues such as this can arise.

Note: An external CALL can use at most 63/64 of the gas currently available at the time of the CALL. Thus, depending on how much gas is required to complete a transaction, a transaction of sufficiently high gas (i.e. one such that 1/64 of the gas is capable of completing the remaining opcodes in the parent call) can be used to mitigate this particular attack.