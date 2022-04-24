# 15) Naught Coin  

Success condition:
> NaughtCoin is an ERC20 token and you're already holding all of them. The catch is that you'll only be able to transfer them after a 10 year lockout period. Can you figure out how to get them out to another address so that you can transfer them freely? Complete this level by getting your token balance to 0.

The contract we have to attack is an implementation of a ERC20 token. It adds a lock modifier to the `transfer()` funtion so we can't transfer anything before a certain date. But ERC20 token have another way of transfering token, the `transferFrom()` function where another contract can call to transfer the token from your account to someone else. But before doing that, that contract need your authorization for the transfer. We can give that authorization via the `approve()` function.

So we create an attack contract. Use `approve()` to give it authorization to transfer our token: `coin.approve(attackContract, coin.INITIAL_SUPPLY(), {"from": account})` and then call the `attack()` function of our contract that will simply transfer itself all of our supply.

---
### ERC20

---
## Level completed!

When using code that's not your own, it's a good idea to familiarize yourself with it to get a good understanding of how everything fits together. This can be particularly important when there are multiple levels of imports (your imports have imports) or when you are implementing authorization controls, e.g. when you're allowing or disallowing people from doing things. In this example, a developer might scan through the code and think that transfer is the only way to move tokens around, low and behold there are other ways of performing the same operation with a different implementation.