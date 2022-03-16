# 3 Coin Flip

> This is a coin flipping game where you need to build up your winning streak by guessing the outcome of a coin flip. To complete this level you'll need to use your psychic abilities to guess the correct outcome 10 times in a row.

So we need to do 10 coin flip and win ten times consecutively. Guessing give us a 1 in 2^10 odds, so we need to find a way to cheat the contract. Luckily for us, getting a random number is extremely hard, even more so with a smart contract.
By looking at the CoinFlip contract, we can see the logic of the RNG. It is based on a constant factor `FACTOR` and the hash of the previous block `blockhash`. The constant factor is know and so is the hash. We need to create a smart contract that will call the `flip()` functioin for us and compute the correct guess.

The `AttackCoinFlip.sol` contract is very simple. First we give the address of the CoinFlip instance to our constructor so our attack contract can interact with its victime. Then we have a single function that will call the `flip()` method with the correct guess. To compute the correct guess we use the same computation as the CoinFlip. Once our contract is written, we deploy it and use a script to call our `flip()` function 10 times.


---
### True randomness
In order to have true randomness in a smart contract, we need to use an oracle such as [Chainlink VRF](https://docs.chain.link/docs/chainlink-vrf/) (Verifiable Random Function)

### blockhash
blockhash(uint blockNumber) returns (bytes32): hash of the given block - only works for 256 most recent blocks