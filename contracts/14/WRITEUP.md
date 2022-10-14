# 14) Gatekeeper Two

Success condition:
> This gatekeeper introduces a few new challenges. Register as an entrant to pass this level.

Similar to the last level we need to pass three gates. The first one is the same as the last level, we just need a contract to act as a middleman. The second gate use `assembly`. The thrid one is simply a bitwise XOR operator.

### Gate One

```require(msg.sender != tx.origin)```


We create an attack contract: `AttackGatekeeperOne.sol`.

### Gate Two
```
uint256 x;
        assembly {
            x := extcodesize(caller())
        }
        require(x == 0);
        _;
```
`extcodesize(a)` is the size of a, `caller()` is our contract calling the enter function. We want the size of the contract to be 0 so we just put all of our code in the contructor. When we create a contract, we immediatley run the constructor of this contract before doing anything else so if the constructor call the `enter()` function the size of our contract is still zero, nothing has been initiated.

> Note that while the initialisation code is executing, the newly created address exists but with no intrinsic body code[5]  
[5] During initialization code execution, EXTCODESIZE on the address should return zero, which is the length of the code of the account while
CODESIZE should return the length of the initialization code.  
> -- <cite>[Ethereum Yellow Paper, chapter 7](https://ethereum.github.io/yellowpaper/paper.pdf)</cite>

### Gate Three

```
require(
        uint64(bytes8(keccak256(abi.encodePacked(msg.sender)))) ^
            uint64(_gateKey) ==
            uint64(0) - 1
        );
```

We use a property of the bitwise XOR operator (`^`): a ^ x = b => a ^ b = x.
So we take the address of our contract (`address(this)`) and XOR it with `uint64(0) - 1` which give us our key.

---
### msg.sender vs tx.origin
Like in a previous challenge, msg.sender is whoever call a given function, either a EOA or a contract, and tx.origin is whoever is at the origin of the transaction, always an EOA.

### Bitwise operations
Bit operators: `&`, `|`, `^` (bitwise exclusive or), `~` (bitwise negation)

---
## Level completed!

Way to go! Now that you can get past the gatekeeper, you have what it takes to join theCyber, a decentralized club on the Ethereum mainnet. Get a passphrase by contacting the creator on reddit or via email and use it to register with the contract at gatekeepertwo.thecyber.eth (be aware that only the first 128 entrants will be accepted by the contract).