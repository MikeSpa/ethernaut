# 5) Token
Success condition:
> The goal of this level is for you to hack the basic token contract below.

> You are given 20 tokens to start with and you will beat the level if you somehow manage to get your hands on any additional tokens. Preferably a very large amount of tokens.

We need to acquire some token. We can see that the contract uses solidity version 0.6.0 and do not use SafeMath. Version of solidity older than 0.8.0 are vulnerable to uint overflow. We need to abuse this vulnerability to change the balances mapping.

If we transfer an amount of 21 token `balances[msg.sender] - _value >= 0` will be true and `balances[msg.sender] -= _value` will actually increase our balance. uint256 have a range of [0, 2^256-1]. since we have 20 token in our account we choose _value to be equla to 21 resulting in:
```
balances[msg.sender] - _value // 20 - 21 = 2^256 -1
```
The uint256 will underflow and give us a huge number for our new balance.

In the console, we simply call the transfer function of Token with any address as a first argument(here the contracts) and 21 as the value.

> `contract.transfer(contract.address, 21)`

We can then check that our balance has increased:

> `await contract.balanceOf(player)`
---
### Overflow
If working with a version of solidity below 0.8.0, always use SafeMath to avoid overflow.
Since 0.8.0, Solidity check for overflow by default and throw an error if one occurs.

---
## Level completed!

Overflows are very common in solidity and must be checked for with control statements such as:
```
if(a + c > a) {
  a = a + c;
}
```
An easier alternative is to use OpenZeppelin's SafeMath library that automatically checks for overflows in all the mathematical operators. The resulting code looks like this:

```
a = a.add(c);
```
If there is an overflow, the code will revert.