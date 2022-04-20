# 13) Gatekeeper One

Success condition:
> Make it past the gatekeeper and register as an entrant to pass this level.

We need to pass the three modifier. Modifier gateOne simply require that the `msg.sender` is different from `tx.origin`. We can easily pass that by having a contract call the GatekeeperOne instance. Modifier gateTwo require a specific gaz amount left, we can determine how much gaz to sent in order of having the wanted gas left when we enter the second modifier. Modifier gateThree require a specific key that pass different conditions based on the our EOA address.

### Gate One

```require(msg.sender != tx.origin)```


We create an attack contract: `AttackGatekeeperOne.sol`.

### Gate Two
```require(gasleft().mod(8191) == 0);```


We need to play with the amount of gas.

### Gate Three

.

---
### msg.sender vs tx.origin
Like in a previous challenge, msg.sender is whoever call a gicen function, either a EOA or a contract, and tx.origin is whoever is at the origin of the transaction, always an EOA.




---
## Level completed!
