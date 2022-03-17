# 4) Telephone

Success Condition:
> Claim ownership of the contract below to complete this level.

Once again we simply need to take ownership of the contract. The contract only contains one function and that function can change ownership, we just need to pass the condition  `if(tx.origin != msg.sender)`. The address in `msg.sender` is whatever address call this function, the `tx.origin` is the address that originally started the transaction.

To have these two being different, we use our `AttackTelephone.sol` contract as a middleman.

We first call our `AtackTelephone.sol` contract that will then call the Telephone instance. For the Telephone contract, `tx.origin` will be our EOA's address and `msg.sender` will be our AttackTelephone contract's address. Telephone will then change the owner to the parameter passed by our contract `changeOwner()` function.

tldr: If contract A calls B, and B calls C, in C `msg.sender` is B and `tx.origin` is A.

---
### tx.origin
tx.origin should never be used for authentication purposes, use msg.sender instead.

---
While this example may be simple, confusing tx.origin with msg.sender can lead to phishing-style attacks.

An example of a possible attack is outlined below.

Use tx.origin to determine whose tokens to transfer, e.g.
```
function transfer(address _to, uint _value) {
  tokens[tx.origin] -= _value;
  tokens[_to] += _value;
}
```
Attacker gets victim to send funds to a malicious contract that calls the transfer function of the token contract, e.g.
```
function () payable {
  token.transfer(attackerAddress, 10000);
}
```
In this scenario, tx.origin will be the victim's address (while msg.sender will be the malicious contract's address), resulting in the funds being transferred from the victim to the attacker.
