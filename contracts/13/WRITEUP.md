# 13) Gatekeeper One

Success condition:
> Make it past the gatekeeper and register as an entrant to pass this level.

We need to pass the three modifier. Modifier gateOne simply require that the `msg.sender` is different from `tx.origin`. We can easily pass that by having a contract call the GatekeeperOne instance. Modifier gateTwo require a specific gaz amount left, we can determine how much gas to sent in order of having the wanted gas left when we enter the second modifier. Modifier gateThree require a specific key that pass different conditions based on the our EOA address.

### Gate One

```require(msg.sender != tx.origin)```


We create an attack contract: `AttackGatekeeperOne.sol`.

### Gate Two
```require(gasleft().mod(8191) == 0);```


We need to play with the amount of gas. Instead of trying to calculate exactly how much gas we had spent until this point I decided to brute force it.

```
for (uint256 i = 0; i < 8191; i++) {  // loop 
            (bool result, ) = victim.call{gas: 24000 + i}(  // modify the gas by one
                abi.encodeWithSignature(("enter(bytes8)"), key)  // call the fct enter with our key
            );
            if (result) { // if call success (no revert)
                break;  // end the loop
            }
        }
```

### Gate Three

We need to find an 8 bytes key with three condition:
 - `uint32(uint64(_gateKey)) == uint16(uint64(_gateKey))`
        -> bits 16 to 32 need to be 0
        -> so 0x0000
 - `uint32(uint64(_gateKey)) != uint64(_gateKey)`
        -> bits 32 to 64 cannot be all 0
        -> can be anything we want except 0x00000000, let's choose 0x6d696b65
 - `uint32(uint64(_gateKey)) == uint16(tx.origin)`
        -> bits 0 to 16 need to be the same as tx.origin (and 16 to 32 need to be 0 (condition 1))
        -> so 0xFFFF

We use the bitwise and operators (`&`) with the mask we just created to get our key: tx.origin & 0x6d696b650000FFFF

---
### msg.sender vs tx.origin
Like in a previous challenge, msg.sender is whoever call a gicen function, either a EOA or a contract, and tx.origin is whoever is at the origin of the transaction, always an EOA.

### Bitwise operations
Bit operators: `&`, `|`, `^` (bitwise exclusive or), `~` (bitwise negation)

---
## Level completed!

Well done! Next, try your hand with the second gatekeeper...