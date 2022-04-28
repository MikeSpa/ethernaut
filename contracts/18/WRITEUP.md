# 18) MagicNumber

Success condition:
> To solve this level, you only need to provide the Ethernaut with a Solver, a contract that responds to whatIsTheMeaningOfLife() with the right number.  
Easy right? Well... there's a catch.  
The solver's code needs to be really tiny. Really reaaaaaallly tiny. Like freakin' really really itty-bitty tiny: 10 opcodes at most.  
Hint: Perhaps its time to leave the comfort of the Solidity compiler momentarily, and build this one by hand O_o. That's right: Raw EVM bytecode.  
Good luck!  

Solidity is a high-level programming language that we need to compile to bytes so the EVM can undestand it. The bytecode gets executed as a number of opcodes.
There is two sets of opcodes: initialization opcodes which create the contract and store the second types of opcodes, runtime opcodes, which is the actual logic of your contract. It is the runtime opcodes that should be 10 opcodes at most.


## Runtimes opcodes
`PUSH1` = 0x60: push 1 byte on the stack
`MSTORE` = 0x52: store on the MEM
`RETURN` = 0xf3: return a value

We need to return the right number, i.e. [42](https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy#Answer_to_the_Ultimate_Question_of_Life,_the_Universe,_and_Everything_(42)). In order to return a value, we must first store that value (1) and then return it (2).
(1) Let's first store the return value (40 = 0x2a) in memory. We need to use the `MSTORE` opcode, the position we want to store the value (Let's take 0x00) and the value (0x2a).
    - We first `PUSH1` the value we want to store on the stack: push 0x2a -> 602a
    - Then `PUSH1` the place we want to store it: push 0x00 -> 6000
    - and finally the `MSTORE` opcode: mstore -> 52
    
We end up with 602a600052. That is 5 opcodes. We now need to return it.


(2) To return something, we need the `RETURN` opcode, the position of the return value and the size of the value. 
    - The size is 32 bytes (or 0x20 in hex): push 0x20 -> 6020
    - The position is 0x00: push 0x00 -> 6000
    - and the `RETURN` opcode: return -> f3

This second part give us 60206000f3. Another 5 opcodes. Putting both step together we get 602a60005260206000f3.


## Initialization opcodes

Now the initialization opcodes. We want to copy the runtime opcodes. 

The opcodes `CODECOPY` require 3 arguments the destination, the position of the code, and the size of the code. 
    - The size is 10 bytes: push 0x0a -> 600a
    - The position is 0x0c (the initialization opccodes will be 12 bytes in size): push 0x0c -> 600c
    - The destination is let's say 0x20: push 0x20 -> 6020
    - and the `CODECOPY` opcode: codecopy -> 39

Then we need to return the runtime opcodes so like above:
    - The size is 10 bytes: push 0x0a -> 600a
    - The position is 0x20: push 0x20 -> 6020
    - and the `RETURN` opcode: return -> f3

Our initialization opcodes is 600a600c602039600a6020f3

To get our final bytescode, we concat the two string: 0x600a600c602039600a6020f3602a60005260206000f3

---
Very detailed set of [articles](https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-i-introduction-832efd2d7737/) on the EVM.

### EVM opcodes

[List of opcodes](https://ethereum.org/en/developers/docs/evm/opcodes/)

### EVM



### Comparison

If we were to try to complet this challenge by writing a contract in solidity.

Writing a simple contract `SolverWayTooBig.sol` and using the compiler give us a bytecode:
6080604052348015600f57600080fd5b506004361060285760003560e01c806385bb7d6914602d575b600080fd5b60336049565b6040805160ff9092168252519081900360200190f35b602a9056fea26469706673582212208afe4970b1f40fb013ff56473b6e03c03f4fd7c05665e22589712f79a6aea1e764736f6c634300060c0033
with a size of 265, with opcodes:
"opcodes": "PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH1 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x4 CALLDATASIZE LT PUSH1 0x28 JUMPI PUSH1 0x0 CALLDATALOAD PUSH1 0xE0 SHR DUP1 PUSH4 0x85BB7D69 EQ PUSH1 0x2D JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x33 PUSH1 0x49 JUMP JUMPDEST PUSH1 0x40 DUP1 MLOAD PUSH1 0xFF SWAP1 SWAP3 AND DUP3 MSTORE MLOAD SWAP1 DUP2 SWAP1 SUB PUSH1 0x20 ADD SWAP1 RETURN JUMPDEST PUSH1 0x2A SWAP1 JUMP INVALID LOG2 PUSH5 0x6970667358 0x22 SLT KECCAK256 DUP11 INVALID 0x49 PUSH17 0xB1F40FB013FF56473B6E03C03F4FD7C056 PUSH6 0xE22589712F79 0xA6 0xAE LOG1 0xE7 PUSH5 0x736F6C6343 STOP MOD 0xC STOP CALLER ",
This is way too big to pass the level.



---
## Level completed!

Congratulations! If you solved this level, consider yourself a Master of the Universe.

Go ahead and pierce a random object in the room with your Magnum look. Now, try to move it from afar; Your telekinesis habilities might have just started working.

