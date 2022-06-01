# 22) Dex

Success condition:
> The goal of this level is for you to hack the basic DEX contract below and steal the funds by price manipulation.  
You will start with 10 tokens of token1 and 10 of token2. The DEX contract starts with 100 of each token.  
You will be successful in this level if you manage to drain all of at least 1 of the 2 tokens from the contract, and allow the contract to report a "bad" price of the assets.

We can see by looking at the Dex contract, and more precisely at `getSwapPrice()` function that we can exploit the way the swap amount is calculated. The dex start with supply of 100 for each token, and we start with 10 and 10. If we first swap 10 of token1, we will receive 10 of token2. We now have 0-20, But then dex has 110-90. Now when we swap our 20 of token2, the dex will send us (20 * 110 / 90) = 24, according to the `getSwapPrice()` function:
```
return ((amount * IERC20(to).balanceOf(address(this))) /
    IERC20(from).balanceOf(address(this)));
```

Our next swap we give us 24 * 110 / 86 = 30 of token1. As we can see, we can use the low liquidity of the pool to manipulate the price of the two token. As a token supply decrease compare to the other one (in the pool) its value increase, so when we go for a swap we get more of the second token. If we keep going, we get 41 of token1 and finally 65 of token2. Now we are at 0-65, the dex is at 110-45. If we tried to swap our 65 token we should receive 65*100/45 = 158 and since the dex doesn't have enough, the transaction revert here: `IERC20(to).transferFrom(address(this), msg.sender, swapAmount);` We need to calculate how many token to swap to completly emtpy the supply of the other token:
```
uint256 amount = dex.balanceOf(from, address(this));
uint256 amountReceived = dex.getSwapPrice(from, to, amount);
if (amountReceived > 110) {
    newAmount = (amount * 110) / amountReceived;
}
```

After this last swap we shuld have a supply of 110 of one token and 20 of the other. We successfully beat the exchange.

---
### 
---
## Level completed!

The integer math portion aside, getting prices or any sort of data from any single source is a massive attack vector in smart contracts.

You can clearly see from this example, that someone with a lot of capital could manipulate the price in one fell swoop, and cause any applications relying on it to use the the wrong price.

The exchange itself is decentralized, but the price of the asset is centralized, since it comes from 1 dex. This is why we need oracles. Oracles are ways to get data into and out of smart contracts. We should be getting our data from multiple independent decentralized sources, otherwise we can run this risk.

Chainlink Data Feeds are a secure, reliable, way to get decentralized data into your smart contracts. They have a vast library of many different sources, and also offer secure randomness, ability to make any API call, modular oracle network creation, upkeep, actions, and maintainance, and unlimited customization.

Uniswap TWAP Oracles relies on a time weighted price model called TWAP. While the design can be attractive, this protocol heavily depends on the liquidity of the DEX protocol, and if this is too low, prices can be easily manipulated.

Here is an example of getting data from a Chainlink data feed (on the kovan testnet):

```
pragma solidity ^0.6.7;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract PriceConsumerV3 {

    AggregatorV3Interface internal priceFeed;

    /**
     * Network: Kovan
     * Aggregator: ETH/USD
     * Address: 0x9326BFA02ADD2366b30bacB125260Af641031331
     */
    constructor() public {
        priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
    }

    /**
     * Returns the latest price
     */
    function getLatestPrice() public view returns (int) {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }
}
```

