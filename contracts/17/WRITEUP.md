# 17) Recovery

Success condition:
> A contract creator has built a very simple token factory contract. Anyone can create new tokens with ease. After deploying the first token contract, the creator sent 0.5 ether to obtain more tokens. They have since lost the contract address.  
This level will be completed if you can recover (or remove) the 0.5 ether from the lost contract address.

We need to find the lost address of the SimpleToken contract where the ether was sent. Once we have the address, we just need to call the `destroy(address)` function of the SimpleToken contract and `selfdestruct(address)` will send back the ether to any address we want.

## 1st method

We can easily find the lost address with etherscan and looking into the transcation made by the instance level ethernaut give us.

But based on the level completed message, the idea was to find the address programmatically and not with etherscan...

## 2nd method

The second method to find the lost address is by using the fact that contract addresses are deterministically genereted, based on the address of the creator and the nonce. The creator address is the ethernaut Recovery instance and the nonce is 1. It should be zero since its the first thing the contract does but unlike EOA when transaction nonce start at 0 and increase for each transactions, contract nonce is a bit different. It increases only for contract creation and start at 1. So the first contract creation has a nonce of 1.

Now we just need to use a formula to go from these two inputs to the contract address. This python function does just that:

```python
def get_contract_address(sender, nonce=1):  #  for a contract the nonce start at one

    rlp_encoded = rlp.encode([to_bytes(hexstr=sender), nonce])
    return to_checksum_address(keccak(rlp_encoded)[12:])
```

---
### Etherscan
We can easily finc the lost contract address using etherscan, We look at the address of the instance level and find the lost contract address in its transaction

### Deterministic Addresses

A contract address is determinisitcally created based on the address of the account/contract that created the contract and the nonce: address = 20_bytes_on_the_right(keccak(RLP(creator, nonce)))
For an EOA, nonce is simply the transaction nonce, for a contract, its the number of contract created, strating at 1

### Misc
[Website](https://toolkit.abdk.consulting/ethereum#contract-address) with address calculator.

---
## Level completed!

Contract addresses are deterministic and are calculated by keccack256(address, nonce) where the address is the address of the contract (or ethereum address that created the transaction) and nonce is the number of contracts the spawning contract has created (or the transaction nonce, for regular transactions).

Because of this, one can send ether to a pre-determined address (which has no private key) and later create a contract at that address which recovers the ether. This is a non-intuitive and somewhat secretive way to (dangerously) store ether without holding a private key.

An interesting [blog post](http://martin.swende.se/blog/Ethereum_quirks_and_vulns.html) by Martin Swende details potential use cases of this.

If you're going to implement this technique, make sure you don't miss the nonce, or your funds will be lost forever.
