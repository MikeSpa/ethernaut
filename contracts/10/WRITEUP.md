# 10) Re-entrancy

Success condition:
> The goal of this level is for you to steal all the funds from the contract.

Simply enough. Based on the Name of the level, we will have to use a re-entrancy attack to steal the funds.



---
### Re-emtrancy attack




---
## Level completed!

In order to prevent re-entrancy attacks when moving funds out of your contract, use the Checks-Effects-Interactions pattern being aware that call will only return false without interrupting the execution flow. Solutions such as ReentrancyGuard or PullPayment can also be used.

transfer and send are no longer recommended solutions as they can potentially break contracts after the Istanbul hard fork Source 1 Source 2.

Always assume that the receiver of the funds you are sending can be another contract, not just a regular address. Hence, it can execute code in its payable fallback method and re-enter your contract, possibly messing up your state/logic.

Re-entrancy is a common attack. You should always be prepared for it!

 

The DAO Hack
The famous DAO hack used reentrancy to extract a huge amount of ether from the victim contract. See 15 lines of code that could have prevented TheDAO Hack.

