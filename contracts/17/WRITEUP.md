# 17) Recovery

Success condition:
> A contract creator has built a very simple token factory contract. Anyone can create new tokens with ease. After deploying the first token contract, the creator sent 0.5 ether to obtain more tokens. They have since lost the contract address.  
This level will be completed if you can recover (or remove) the 0.5 ether from the lost contract address.

We just need to call the `destroy()` function of the SimpleToken contract and `selfdestruct()` will send us back the ether.

But based on the level completed message, the idea was to find the address programmatically and not with etherscan...

---
### 


---
## Level completed!

Contract addresses are deterministic and are calculated by keccack256(address, nonce) where the address is the address of the contract (or ethereum address that created the transaction) and nonce is the number of contracts the spawning contract has created (or the transaction nonce, for regular transactions).

Because of this, one can send ether to a pre-determined address (which has no private key) and later create a contract at that address which recovers the ether. This is a non-intuitive and somewhat secretive way to (dangerously) store ether without holding a private key.

An interesting blog post by Martin Swende details potential use cases of this.

If you're going to implement this technique, make sure you don't miss the nonce, or your funds will be lost forever.

