# 23) Dex Two

Success condition:
> This level will ask you to break DexTwo, a subtlely modified Dex contract from the previous level, in a different way.  
You need to drain all balances of token1 and token2 from the DexTwo contract to succeed in this level.  
You will still start with 10 tokens of token1 and 10 of token2. The DEX contract still starts with 100 of each token.

This level is similar to the previous one, but we can see that the swap function no longer require the two token to be the two allowed token of the dex. This means we can swap any token we want. We again start with the same balance: the dex start with supply of 100 for each token, and we start with 10 and 10. This time we need to drain the supply of both token form the dex.

We will create a new ERC20 token and swap our own newly make token for the two token present on the dex, we just need to figured out how much to swap to get the entire supply of token 1and 2. If we look at `getSwapAmount()`:

```js
function getSwapAmount(
        address from,
        address to,
        uint256 amount
    ) public view returns (uint256) {
        return ((amount * IERC20(to).balanceOf(address(this))) /
            IERC20(from).balanceOf(address(this)));
    }
```

we can see that if we want 100 of token1 we need `amount / IERC20(from).balanceOf(address(this)))` to be equal to 1. We can simply send 1 of our new token to the exchange and then swap an amount of 1. Then dex will think that the value of 1 of our new token is worth 100 of token1 so it will exchange our 1 token for 100 of token1.

Now that the dex has 2 of my new token, we need to swap 2 of that token in order to receive 100 of token2.
we have drain both token supply from the exchange for the price of 4 useless token.


---
### Dex
An exchange should be careful how it get the true value of a token, either only allowing certain token of having different pool for each pair of token.

---
## Level completed!

As we've repeatedly seen, interaction between contracts can be a source of unexpected behavior.

Just because a contract claims to implement the ERC20 spec does not mean it's trust worthy.

Some tokens deviate from the ERC20 spec by not returning a boolean value from their transfer methods. See Missing return value bug - At least 130 tokens affected.

Other ERC20 tokens, especially those designed by adversaries could behave more maliciously.

If you design a DEX where anyone could list their own tokens without the permission of a central authority, then the correctness of the DEX could depend on the interaction of the DEX contract and the token contracts being traded.

