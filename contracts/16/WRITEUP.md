# 16) Preservation

Success condition:
> This contract utilizes a library to store two different times for two different timezones. The constructor creates two instances of the library for each time to be stored.  
The goal of this level is for you to claim ownership of the instance you are given.

We can see there is no function that can change the owner variable so we will have to find another way. The contract uses a library and two function call this library with `delegatecall()`. By looking at the library, we can see that it has a function to change its first variable. This means we can use the delegate call to change the first variable of our victim contract which happens to be the address of the library. We will change it to our attack contract. Once we change that address, we will be able to tell the contract to call a function in our attack contract, with delegatecall, which we will use to change the owner variable.

```
function attack() public {
    Preservation(victim).setFirstTime(uint256(address(this)));  // we first change the address of lib1 in our victim contract

    Preservation(victim).setFirstTime(7370616872);  //then call this method again with any random parameter it will call setTime below
}

function setTime(uint256 _owner) public {
    owner = tx.origin;  //we now change the owner to our EAO and completed the level
}

```

---
### Library
Declare with the keyword `library`, Library should be use when we want a function to be reuse by other contracts. We don't have to rewrite the code if it already exist somewhere and we can save on gas. They should be stateless, have no variables, cannot be inherited and cannot inherit. They should not be used to change the state of a contract but to do basic operations based on inputs.

### Delegatecall() method
There exists a special variant of a message call, named delegatecall which is identical to a message call apart from the fact that the code at the target address is executed in the context of the calling contract and `msg.sender` and `msg.value` do not change their values.

Good example of a possible hack on [Solidity-by-example](https://solidity-by-example.org/hacks/delegatecall/)

---
## Level completed!

As the previous level, delegate mentions, the use of delegatecall to call libraries can be risky. This is particularly true for contract libraries that have their own state. This example demonstrates why the library keyword should be used for building libraries, as it prevents the libraries from storing and accessing state variables.
