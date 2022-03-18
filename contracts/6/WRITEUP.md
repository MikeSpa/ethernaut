# 6) Delegation

Success condition:
> The goal of this level is for you to claim ownership of the instance you are given.

So we need to gain ownership of the Delegation contract. This one seems already a bit more tricky than the other ones. We can see that the contract has a `fallback()` function. Fallback functions are special function in a solidity contract that get called when no function match the signature of the call. (`receive()` works similarly but when datacall is empty, used to receive ether).

The function first line is `address(delegate).delegatecall(msg.data);`. `delegatecall()` is a function thats works like a regular message call except that the context in which the code is exectued is the one of the calling contract and not the called contract. This means we can call a function of `Delegate.sol` but within the context of the `Delegation.sol` contract instance. The argument given to `delegatecall()` is `msg.data`.

A message call has several field: from, to, gas, gaslimit, and data. `msg.data` allowed the contract to have access to this data field. It's structure is as such:
- The first 4 bytes are the method Id: It is derived from the method we want to call (first 4 bytes of Keccak hash of the signature, i.e. 0xdd365b8b for `pwn()`)
- The rest are for the parameter, either the value of the paramter or its location if the parameter is of dynamic type (array, string,...). But we dont need that for this challenge.

To solve this challenge, we just need to find the keccak_hash of `pwn()` and send it in msg.data to the `Delegation.sol` instance.
> `contract.sendTransaction({data:"0xDD365B8B"})`

This will call the `Delegation.sol` instance fallback()
function which will in turn call the `Delegate` `pwn()` function since our `msg.data` contains its the method id. `pwn()` will change the `owner` variable within the context of `Delegation` instance which will give us ownership. `owner` is the variable in the first slot of `Delegate` storage so it will change the first slot of `Delegation` storage which happen to be owner also.

---

### Fallback() method
A contract can have at most one fallback function, declared using `fallback() external [payable]` (without the function keyword). This function cannot have arguments, cannot return anything and must have external visibility. It is executed on a call to the contract if none of the other functions match the given function signature, or if no data was supplied at all and there is no receive Ether function. The fallback function always receives data, but in order to also receive Ether it must be marked payable.

Even though the fallback function cannot have arguments, one can still use msg.data to retrieve any payload supplied with the call.

### Delegatecall() method
There exists a special variant of a message call, named delegatecall which is identical to a message call apart from the fact that the code at the target address is executed in the context of the calling contract and `msg.sender` and `msg.value` do not change their values.

Good example of a possible hack on [Solidity-by-example](https://solidity-by-example.org/hacks/delegatecall/)

### Msg.data
https://ethereum.stackexchange.com/questions/14037/what-is-msg-data

### Method Id
0xcdcd77c0: the Method ID. This is derived as the first 4 bytes of the Keccak hash of the ASCII form of the signature `baz(uint32,bool)`

### Storage
Each contract has up to 2^256 storage slot of 32 bytes each, in the order of declaration.

---

## Level completed!
Usage of delegatecall is particularly risky and has been used as an attack vector on multiple historic hacks. With it, your contract is practically saying "here, -other contract- or -other library-, do whatever you want with my state". Delegates have complete access to your contract's state. The delegatecall function is a powerful feature, but a dangerous one, and must be used with extreme care.

Please refer to the [The Parity Wallet Hack Explained](https://blog.openzeppelin.com/on-the-parity-wallet-multisig-hack-405a8c12e8f7/) article for an accurate explanation of how this idea was used to steal 30M USD.