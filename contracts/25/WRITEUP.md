# 25) Motorbike

Success condition:
> Ethernaut's motorbike has a brand new upgradeable engine design.  
Would you be able to selfdestruct its engine and make the motorbike unusable ?

We have a proxy pattern with the Engine contract acting as the logic (or implementation) and Motorbike as the proxy contract we are supposed to interact with, which delegate calls to the implementation contract. The address of the implementation contract is saved in a specific storage slot (`_IMPLEMENTATION_SLOT =
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`) to avoid storage collision between the proxy and the implementation. 

We need to make the Motorbike contract unusable. We can see that the Motorbike contract only holds the code to delegate to the implementation and the code to upgrade the implementation is in the Engine contract. This is often done that way to optimize gas cost, you want the proxy to be as small as possible since you will deploy many proxies and the implementation only once, so it can be bigger. But this means that if we can destruct the Engine contract, the Motorbike proxy will become completely unusable, and it will not be possible to change its implementation to a new one.

We are going to call `upgradeToAndCall()` to change the implementation to a new address:
```js
function upgradeToAndCall(address newImplementation, bytes memory data)
        external
        payable
    {
        _authorizeUpgrade();  // check that we are the upgrader
        _upgradeToAndCall(newImplementation, data);  // delegatecall newImpl. with data
    }
```
But for that, we first need to be the `upgrader` of Engine. The only way to change the `upgrader` variable is to call `initialize()`. The `initializer` modifier only allows the function to be called once, by setting an `initialized` variable to `true` and locking the function forever. Unfortunately, the constructor of Motorbike already called it once so if we tried to call `initialize()` on the proxy again, it will fail.  
But when Motorbike::constructor call `initialize()` on its implementation contract with a delegate call, the variables in the initialize function of Engine get written in the proxy storage and not in the implementation storage. The proxy uses the implementation solely for logic and disregard its storage entirely. So now, we have in the proxy: `initialized` is set to `true` and `upgrader` set to the factory contract, but if we look directly in the logic contract, bypassing the proxy, `initialized` is set to `false` and `upgrader` to `0x00` so we can then call `initialize()` and change the `upgrader` to our address.  
Now that we are the `upgrader` (in the implementation contract) we can call `upgradeToAndCall()`. `upgradeToAndCall(newImplementation, data)` will delegatecall the given address with the given parameter data: `newImplementation.delegatecall(data);`. What we want to do is completely destruct the implementation contract. We create a new contract with a single function called `destruct()` that will call `selfdestruct()`. By making the contract call our `destruct()` function, the implementation will selfdestruct since the implementation uses a `delegatecall()`.  
The proxy is completely unaware of what we have been doing, it still points to the engine implementation address for its logic but this address no longer has a contract, meaning that when someone calls the proxy it will try to delegate the call to a contract that no longer exist and the call will fail. Since the logic to upgrade the implementation was in that contract, it is no longer possible to upgrade and the proxy is unusable.


---
### Storage

The main aspect of this challenge is to understand how storage works in a proxy pattern. When Motorbike::constructor call initialize() on its implementation contract with a delegate call, the value in the initialize function of Engine gets written in the proxy storage and not in the implementation storage. The proxy uses the implementation solely for logic and disregard its storage entirely. Since the Engine contract has a initialize function (instead of a constructor) that anyone can call, anyone can change the variable stored in this contract. And when you call the contract without going through the proxy, the context is the one of the implementation contract.

### UUP
[UUPS Proxies: A Tutorial](https://forum.openzeppelin.com/t/uups-proxies-tutorial-solidity-javascript/7786)  
[EIP-1822: Universal Upgradeable Proxy Standard (UUPS)](https://eips.ethereum.org/EIPS/eip-1822)

### Initializable

Helper contract to support initializer functions. To use it, replace the constructor with a function that has the `initializer` modifier. Solidity takes care of automatically invoking the constructors of all ancestors of a contract. When writing an initializer, you need to take special care to manually call the initializers of all parent contracts.
Here we use the fact that `initialize()` function can be called at anytime, unlike a constructor.

[code](https://github.com/OpenZeppelin/openzeppelin-upgrades/blob/master/packages/core/contracts/Initializable.sol)


---
## Level completed!

The advantage of following an UUPS pattern is to have very minimal proxy to be deployed. The proxy acts as storage layer so any state modification in the implementation contract normally doesn't produce side effects to systems using it, since only the logic is used through delegatecalls.

This doesn't mean that you shouldn't watch out for vulnerabilities that can be exploited if we leave an implementation contract uninitialized.

This was a slightly simplified version of what has really been discovered after months of the release of UUPS pattern.

Takeways: never leaves implementation contracts uninitialized ;)

If you're interested in what happened, read more [here](https://forum.openzeppelin.com/t/uupsupgradeable-vulnerability-post-mortem/15680).

