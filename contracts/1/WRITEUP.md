# 1 Fallout

We need to take ownership of the contract and withdraw its balance.

We can see that the fallback function `receive()` changes the `owner` to `msg.sender`. The function first check two condition in `require()`: we need to call receive() with a `msg.value` greater than zero and we need to have already made a contribution. We first make that contribution with:

 > ```contract.contribute({value:1})```

and then call the `receive()` function.
The receive() function is new in solidity 0.0.6. Per [this article](https://blog.soliditylang.org/2020/03/26/fallback-receive-split/): 'It executes on calls to the contract with no data (calldata)'. We thus call:

> ```contract.sendTransaction({value:1})```

We are now the owner of the contract, this allow us to call `withdraw()` and empty the contract:

> ```contract.withdraw()```
