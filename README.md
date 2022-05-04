# Solution to the [Ethernaut](https://ethernaut.openzeppelin.com/) challenges

Simple writeup of the different level of the Ethernaut wargame.

For each level, there is a small writeup to understand the vulnerabilities and how to exploit them, plus supplemental information about how solidity works. 
Each level also has a brownie script to test the hack locally and on the real level instance on the rinkeby testnet. 
When necessary, attack contract are also provided. I tried to use solidity contract as much as possible to attack instead of relying on Web3 command.

# 1 Fallout

We need to take ownership of the contract and withdraw its balance.

We can see that the fallback function `receive()` changes the `owner` to `msg.sender`. The function first check two condition in `require()`: we need to call receive() with a `msg.value` greater than zero and we need to have already made a contribution. We first make that contribution with:

 > ```contract.contribute({value:1})```

and then call the `receive()` function.
The receive() function is new in solidity 0.0.6. Per [this article](https://blog.soliditylang.org/2020/03/26/fallback-receive-split/): 'It executes on calls to the contract with no data (calldata)'. We thus call:

> ```contract.sendTransaction({value:1})```

We are now the owner of the contract, this allow us to call `withdraw()` and empty the contract:

> ```contract.withdraw()```

# 2 Fallout

Here again, we simply need to take ownership of the contract. We can see that the "constructor" function is actually a regular function and thus callable by anyone. Calling it will change the `owner` to `msg.sender` and we are already done:

> ```contract.Fal1out()```

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

# 5) Token
Success condition:
> The goal of this level is for you to hack the basic token contract below.

> You are given 20 tokens to start with and you will beat the level if you somehow manage to get your hands on any additional tokens. Preferably a very large amount of tokens.

We need to acquire some token. We can see that the contract uses solidity version 0.6.0 and do not use SafeMath. Version of solidity older than 0.8.0 are vulnerable to uint overflow. We need to abuse this vulnerability to change the balances mapping.

If we transfer an amount of 21 token `balances[msg.sender] - _value >= 0` will be true and `balances[msg.sender] -= _value` will actually increase our balance. uint256 have a range of [0, 2^256-1]. since we have 20 token in our account we choose _value to be equla to 21 resulting in:
```
balances[msg.sender] - _value // 20 - 21 = 2^256 -1
```
The uint245 will underflow and give us a huge number for our new balance.

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

# 6) Delegation

Success condition:
> The goal of this level is for you to claim ownership of the instance you are given.

So we need to gain ownership of the Delegation contract. This one seems already a bit more tricky than the other ones. We can see that the contract has a `fallback()` function. Fallback functions are special function in a solidity contract that get called when no function match the signature of the call. (`receive()` works similarly but when datacall is empty, used to receive ether).

The function first line is `address(delegate).delegatecall(msg.data);`. `delegatecall()` is a function thats works like a regular message call except that the context in which the code is exectued is the one of the calling contract and not the called contract. This means we can call a function of `Delegate.sol` but within the context of the `Delegation.sol` contract instance. The argument given to `delegatecall()` is `msg.data`.

A message call has several field: from, to, gas, gaslimit, and data. `msg.data` allowed the contract to have access to this data field. It's structure is as such:
- The first 4 bytes are the method Id: It is derived from the method we want to call (first 4 bytes of Keccak hash of the signature, i.e. 0xdd365b8b for `pwn()`)
- The rest are for the parameter, either the value of the paramter or its location if the parameter is of dynamic type (array, string,...). But we dont need that for this challenge.

To solve this challenge, we just need to find the keccak_hash of `pwn()` and send it in msg.data to the `Delegation.sol` instance.
> `contract.sendTransaction({data:"0xDD365B8B"})`

This will call the `Delegation.sol` instance fallback()
function which will in turn call the `Delegate` `pwn()` function since our `msg.data` contains its the method id. `pwn()` will change the `owner` variable within the context of `Delegation` instance which will give us ownership. `owner` is the variable in the first slot of `Delegate` storage so it will change the first slot of `Delegation` storage which happen to be owner also.

---

### Fallback() method
A contract can have at most one fallback function, declared using `fallback() external [payable]` (without the function keyword). This function cannot have arguments, cannot return anything and must have external visibility. It is executed on a call to the contract if none of the other functions match the given function signature, or if no data was supplied at all and there is no receive Ether function. The fallback function always receives data, but in order to also receive Ether it must be marked payable.

Even though the fallback function cannot have arguments, one can still use msg.data to retrieve any payload supplied with the call.

### Delegatecall() method
There exists a special variant of a message call, named delegatecall which is identical to a message call apart from the fact that the code at the target address is executed in the context of the calling contract and `msg.sender` and `msg.value` do not change their values.

Good example of a possible hack on [Solidity-by-example](https://solidity-by-example.org/hacks/delegatecall/)

### Msg.data
https://ethereum.stackexchange.com/questions/14037/what-is-msg-data

### Method Id
0xcdcd77c0: the Method ID. This is derived as the first 4 bytes of the Keccak hash of the ASCII form of the signature `baz(uint32,bool)`

### Storage
Each contract has up to 2^256 storage slot of 32 bytes each, in the order of declaration.

---

## Level completed!
Usage of delegatecall is particularly risky and has been used as an attack vector on multiple historic hacks. With it, your contract is practically saying "here, -other contract- or -other library-, do whatever you want with my state". Delegates have complete access to your contract's state. The delegatecall function is a powerful feature, but a dangerous one, and must be used with extreme care.

Please refer to the [The Parity Wallet Hack Explained](https://blog.openzeppelin.com/on-the-parity-wallet-multisig-hack-405a8c12e8f7/) article for an accurate explanation of how this idea was used to steal 30M USD.

# 7) Force

Success condition:
> Some contracts will simply not take your money ¯\_(ツ)_/¯

>The goal of this level is to make the balance of the contract greater than zero.

The main way to send ether to a smart contract is by calling a `payable` function. `Force.sol` doesn't have one. There a a few other way to force a smart contract to take our ether. One one them is with `selfdestruc()`.

`selfdestruct()` is a special method that destroy a smart contract and send its ether balance to a given address. If we create a contract with a function that call `selfdestruct()` and with the `Force.sol` instance address as its receiver, send it some eth and then call destruct the contract, you will have sent ether to our target contract.

---
### selfdestruct()
The only way to remove code from the blockchain is when a contract at that address performs the selfdestruct operation. The remaining Ether stored at that address is sent to a designated target and then the storage and code is removed from the state. Removing the contract in theory sounds like a good idea, but it is potentially dangerous, as if someone sends Ether to removed contracts, the Ether is forever lost.

### Force a contract to receive ether
[StackExchange](https://ethereum.stackexchange.com/questions/63987/can-a-contract-with-no-payable-function-have-ether)

---
## Level completed

In solidity, for a contract to be able to receive ether, the fallback function must be marked payable.

However, there is no way to stop an attacker from sending ether to a contract by self destroying. Hence, it is important not to count on the invariant address(this).balance == 0 for any contract logic.

# 8) Vault

Success condition:
> Unlock the vault to pass the level!

To pass the challenge, we need to find the password. It is saved on the contract in a `private` variable. But despite it being private, everything in a smart contract is still accessible.

Just call `web.eth.getStorageAt(contract.address, 1)` and pass that to `unlock()`

---
### Visibility
public: visible externally and internally (creates a getter function for storage/state variables)

private: only visible in the current contract

external: only visible externally (only for functions) - i.e. can only be message-called (via this.func)

internal: only visible internally

### Private
Making something private or internal only prevents other contracts from reading or modifying the information, but it will still be visible to the whole world outside of the blockchain.

### GetStorageAt
Eth.get_storage_at(account, position, block_identifier=eth.default_block)
 - Delegates to eth_getStorageAt RPC Method

Returns the value from a storage position for the given account at the block specified by block_identifier.

> web3.eth.get_storage_at('0x6C8f2A135f6ed072DE4503Bd7C4999a1a17F824B', 0)
'0x00000000000000000000000000000000000000000000000000120a0b063499d4'

---
# Level completed

It's important to remember that marking a variable as private only prevents other contracts from accessing it. State variables marked as private and local variables are still publicly accessible.

To ensure that data is private, it needs to be encrypted before being put onto the blockchain. In this scenario, the decryption key should never be sent on-chain, as it will then be visible to anyone who looks for it. zk-SNARKs provide a way to determine whether someone possesses a secret parameter, without ever having to reveal the parameter.

# Misc

When deploying and destructing a contract with brownie, make sure to remove its abi .json file from the build/deployments/<chain-id> folder or brownie will crash with `ContractNotFound: No contract deployed at 0x...` and if at the same time rinkeby is fucking struggling and etherscan is down plus the script works fine on other network, one might be inclined to believe that the problem come from rinkeby and not that destroy contract, and stupidely wait almost a week to completed an easy level.


# 9) King

Success condition:
> The contract below represents a very simple game: whoever sends it an amount of ether that is larger than the current prize becomes the new king. On such an event, the overthrown king gets paid the new prize, making a bit of ether in the process! As ponzi as it gets xD

> Such a fun game. Your goal is to break it.

> When you submit the instance back to the level, the level is going to reclaim kingship. You will beat the level if you can avoid such a self proclamation.

We need to block the level from taking back kingship of the instance. Once we submit the instance it will call the receive fct:

```
require(msg.value >= prize || msg.sender == owner);
king.transfer(msg.value);
king = msg.sender;  // becomes the new king
prize = msg.value;
```

In order to block that from happening, we need to make sure this function revert. We can do that by making the transfer line revert. If we make a contract with no receive fct king, it will be impossible to transfer ether to it and this fct will revert and our contract will stay king forever.

---


# 10) Re-entrancy

Success condition:
> The goal of this level is for you to steal all the funds from the contract.

Simply enough. Based on the Name of the level, we will have to use a re-entrancy attack to steal the funds. We can see that this line `msg.sender.call{value: _amount}("")` in the withdraw function will send ehter to the `msg.sender`. If the `msg.sender` is a contract, this will call the `receive()` function. We can thus choose to execute any code we want within this function. This is how we will attack this contract.

Our `receive()` function is like this:

```
receive() external payable {
    uint256 balanceTotal = victim.balance; // find out how much ether is in the contract
    if (balanceTotal > 0) {
        Reentrance(victim).withdraw(balanceTotal); // withdraw all of it
    }
    owner.transfer(address(this).balance);  // send the ether to the attacker address (whoever deploy the attack contract)
}

```

By looking at the `withdraw()` function we can see that we need to satisfy this condition `(balances[msg.sender] >= _amount)` to execute the `msg.sender.call()`. So we first need to donate some ether to increase our balance in the contract. By sending the same amount of ether that is on the contract, We will be able to drain all funds by calling the `withdraw()` function:

```
function attack() public {
    uint256 balanceTotal = victim.balance;  //get the amount of ether on the contract
    Reentrance(victim).donate{value: balanceTotal, gas: 1000000}( //send that much ether.  (need to add more gaz)
        address(this)
    );
    Reentrance(victim).withdraw(balanceTotal);  // withdraw the same amount
}

```
Here's what happens during our attack in the Reentrance::withdraw function:
```
   function withdraw(uint256 _amount) public {
        if (balances[msg.sender] >= _amount) {  // 1. condition passed since withdraw what we sent
            (bool result, ) = msg.sender.call{value: _amount}("");  // 2. we get our money back plus run our receive() function which run 1. and 2. again
            if (result) {
                _amount;
            }
            balances[msg.sender] -= _amount;
        }
    }

```




---
### Re-entrancy attack

A contract during its normal execution may perform calls to other contracts, by doing function calls or simply transferring Ether. These contracts can themselves call other contracts. In particular, they can call back to the contract that called them, or any other in the call stack. In that case, we say that the contract is re-entered, and this situation is known as reentrancy.



### How to prevent the attack
To avoid a Re-entrancy attack, it is good to use a Check-effect-interaction pattern, where you first reduce the balance of the user before sending him his money for exemple. You can also use a lock on the function such as a locking modifier:
```
modifier lock() {
        locked = true;
        _;
        locked = false;
    }
```

### call() instead of transfer and send
```
contract Vulnerable {
    function withdraw(uint256 amount) external {
        // This forwards 2300 gas, which may not be enough if the recipient
        // is a contract and gas costs change.
        msg.sender.transfer(amount);
    }
}

contract Fixed {
    function withdraw(uint256 amount) external {
        // This forwards all available gas. Be sure to check the return value!
        (bool success, ) = msg.sender.call.value(amount)("");
        require(success, "Transfer failed.");
    }
}
```

---
## Level completed!

In order to prevent re-entrancy attacks when moving funds out of your contract, use the Checks-Effects-Interactions pattern being aware that call will only return false without interrupting the execution flow. Solutions such as ReentrancyGuard or PullPayment can also be used.

transfer and send are no longer recommended solutions as they can potentially break contracts after the Istanbul hard fork [Source 1](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/), [Source 2](https://forum.openzeppelin.com/t/reentrancy-after-istanbul/1742).

Always assume that the receiver of the funds you are sending can be another contract, not just a regular address. Hence, it can execute code in its payable fallback method and re-enter your contract, possibly messing up your state/logic.

Re-entrancy is a common attack. You should always be prepared for it!

 

The DAO Hack
The famous DAO hack used reentrancy to extract a huge amount of ether from the victim contract. See 15 lines of code that could have prevented TheDAO Hack.

# 11) Elevator

Succes condition:
> This elevator won't let you reach the top of your building. Right?

We just need to set the `top` variable to `true`. The function `goTo()` can do that:

```
function goTo(uint256 _floor) public {
    Building building = Building(msg.sender);  //our contract need to be a Building

    if (!building.isLastFloor(_floor)) {  // isLastFloor need to be false
        floor = _floor;
        top = building.isLastFloor(floor);  // now isLastFloor need to be true
    }
}
```
So we just need to create a contract with a `isLastFloor(uint256)` function that return `false` the first time it is called and `true` the second time. This easily do the trick:

```
function isLastFloor(uint256 _floor) external returns (bool) {
    bool ret = top;
    top = !top;
    return ret;
}
```

---
Don't really understand what there is to learn here though.

---
## Level completed!

You can use the view function modifier on an interface in order to prevent state modifications. The pure modifier also prevents functions from modifying the state. Make sure you read Solidity's documentation and learn its caveats.

An alternative way to solve this level is to build a view function which returns different results depends on input data but don't modify state, e.g. gasleft().


# 12) Privacy

Success condition:
> The creator of this contract was careful enough to protect the sensitive areas of its storage.  
Unlock this contract to beat the level.

Just like for the 8th level, we need to find out what is written in a variable to unlock the contract. Since the variable is priavate we can't access it via a getter. We need to figure out where is the storage slot the key is and retrieve it with GetStorageAt. Smart contract storage have 2^256 32bytes slots. it two consecutive variable can fit in one slot they are packed together from right to left. Once we know what is in data[2] we need to cast it in bytes16. I used a contract to cast the data in bytes16. So we jsut need to call the `attack()` function with data that we get from `getStorageAt()`.

---
### Solidity Storage

        <-         32 bytes                   ->  
Variable0: __________________________________| Bool|  
Variable1: ---------------------------uint256--------------------------|    
Variable2: __________________________________| uint8|  
Variable3: __________________________________| uint8|  
Variable4: _______________________| -------uint16---------|  
Variable5: -------------------------bytes32[0]------------------------|    
Variable6: -------------------------bytes32[0]------------------------|    
Variable7: -------------------------bytes32[0]------------------------|    
Variable8: ________________________________________|  

Storage:
        <-         32 bytes                   ->  
Slot_0: __________________________________| Bool|  
Slot_1: ---------------------------uint256--------------------------|    
Slot_2: | ----------uint16------------||--- uint8---||---uint8---|  
Slot_5: -------------------------bytes32[0]------------------------|    
Slot_6: -------------------------bytes32[0]------------------------|    
Slot_7: -------------------------bytes32[0]------------------------|    
Slot_8: ________________________________________|  


---
## Level completed!

Nothing in the ethereum blockchain is private. The keyword private is merely an artificial construct of the Solidity language. Web3's getStorageAt(...) can be used to read anything from storage. It can be tricky to read what you want though, since several optimization rules and techniques are used to compact the storage as much as possible.

It can't get much more complicated than what was exposed in this level. For more, check out this excellent article by "Darius": [How to read Ethereum contract storage](https://medium.com/aigang-network/how-to-read-ethereum-contract-storage-44252c8af925)

# 13) Gatekeeper One

Success condition:
> Make it past the gatekeeper and register as an entrant to pass this level.

We need to pass the three modifier. Modifier gateOne simply require that the `msg.sender` is different from `tx.origin`. We can easily pass that by having a contract call the GatekeeperOne instance. Modifier gateTwo require a specific gaz amount left, we can determine how much gas to sent in order of having the wanted gas left when we enter the second modifier. Modifier gateThree require a specific key that pass different conditions based on the our EOA address.

### Gate One

```require(msg.sender != tx.origin)```


We create an attack contract: `AttackGatekeeperOne.sol`.

### Gate Two
```require(gasleft().mod(8191) == 0);```


We need to play with the amount of gas. Instead of trying to calculate exactly how much gas we had spent until this point I decided to brute force it.

```
for (uint256 i = 0; i < 8191; i++) {  // loop 
            (bool result, ) = victim.call{gas: 24000 + i}(  // modify the gas by one
                abi.encodeWithSignature(("enter(bytes8)"), key)  // call the fct enter with our key
            );
            if (result) { // if call success (no revert)
                break;  // end the loop
            }
        }
```

### Gate Three

We need to find an 8 bytes key with three condition:
 - `uint32(uint64(_gateKey)) == uint16(uint64(_gateKey))`
        -> bits 16 to 32 need to be 0
        -> so 0x0000
 - `uint32(uint64(_gateKey)) != uint64(_gateKey)`
        -> bits 32 to 64 cannot be all 0
        -> can be anything we want except 0x00000000, let's choose 0x6d696b65
 - `uint32(uint64(_gateKey)) == uint16(tx.origin)`
        -> bits 0 to 16 need to be the same as tx.origin (and 16 to 32 need to be 0 (condition 1))
        -> so 0xFFFF

We use the bitwise and operators (`&`) with the mask we just created to get our key: tx.origin & 0x6d696b650000FFFF

---
### msg.sender vs tx.origin
Like in a previous challenge, msg.sender is whoever call a gicen function, either a EOA or a contract, and tx.origin is whoever is at the origin of the transaction, always an EOA.

### Bitwise operations
Bit operators: `&`, `|`, `^` (bitwise exclusive or), `~` (bitwise negation)

---
## Level completed!

Well done! Next, try your hand with the second gatekeeper...


# 14) Gatekeeper Two

Success condition:
> This gatekeeper introduces a few new challenges. Register as an entrant to pass this level.

Similar to the last level we need to pass three gates. The first one is the same as the last level, we just need a contract to act as a middleman. The second gate use `assembly`. The thrid one is simply a bitwise XOR operator.

### Gate One

```require(msg.sender != tx.origin)```


We create an attack contract: `AttackGatekeeperOne.sol`.

### Gate Two
```
uint256 x;
        assembly {
            x := extcodesize(caller())
        }
        require(x == 0);
        _;
```
`extcodesize(a)` is the size of a, `caller()` is our contract calling the enter function. We want the size of the contract to be 0 so we just put all of our code in the contructor. When we create a contract, we immediatley run the constructor of this contract before doing anything else so if the constructor call the `enter()` function the size of our contract is still zero, nothing has been initiated.

> Note that while the initialisation code is executing, the newly created address exists but with no intrinsic body code[5]  
[5] During initialization code execution, EXTCODESIZE on the address should return zero, which is the length of the code of the account while
CODESIZE should return the length of the initialization code.  
> -- <cite>[Ethereum Yellow Paper, chapter 7](https://ethereum.github.io/yellowpaper/paper.pdf)</cite>

### Gate Three

```
require(
        uint64(bytes8(keccak256(abi.encodePacked(msg.sender)))) ^
            uint64(_gateKey) ==
            uint64(0) - 1
        );
```

We use a property of the bitwise XOR operator (`^`): a ^ x = b => a ^ b = x.
So we take the address of our contract (`address(this)`) and XOR it with `uint64(0) - 1` which give us our key.

---
### msg.sender vs tx.origin
Like in a previous challenge, msg.sender is whoever call a gicen function, either a EOA or a contract, and tx.origin is whoever is at the origin of the transaction, always an EOA.

### Bitwise operations
Bit operators: `&`, `|`, `^` (bitwise exclusive or), `~` (bitwise negation)

---
## Level completed!

Way to go! Now that you can get past the gatekeeper, you have what it takes to join theCyber, a decentralized club on the Ethereum mainnet. Get a passphrase by contacting the creator on reddit or via email and use it to register with the contract at gatekeepertwo.thecyber.eth (be aware that only the first 128 entrants will be accepted by the contract).


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


# 16) Preservation

Success condition:
> This contract utilizes a library to store two different times for two different timezones. The constructor creates two instances of the library for each time to be stored.  
The goal of this level is for you to claim ownership of the instance you are given.

We can see there is no function that can change the owner variable so we will have to find another way. The contract uses a library and two function call this library with `delegatecall()`. By looking at the library, we can see that it has a function to change its first variable. This means we can use the delegate call to change the first variable of our victim contract which happens to be the address of the library. We will change it to our attack contract. Once we change that address, we will be able to tell the contract to call a function in our attack contract, with delegatecall, which we will use to change the owner variable.

```
function attack() public {
    Preservation(victim).setFirstTime(uint256(address(this)));  // we first change the address of lib1 in our victim contract

    Preservation(victim).setFirstTime(7370616872);  //then call this method again with any random parameter it will call setTime below
}

function setTime(uint256 _owner) public {
    owner = tx.origin;  //we now change the owner to our EAO and completed the level
}

```

---
### Library
Declare with the keyword `library`, Library should be use when we want a function to be reuse by other contracts. We don't have to rewrite the code if it already exist somewhere and we can save on gas. They should be stateless, have no variables, cannot be inherited and cannot inherit. They should not be used to change the state of a contract but to do basic operations based on inputs.

### Delegatecall() method
There exists a special variant of a message call, named delegatecall which is identical to a message call apart from the fact that the code at the target address is executed in the context of the calling contract and `msg.sender` and `msg.value` do not change their values.

Good example of a possible hack on [Solidity-by-example](https://solidity-by-example.org/hacks/delegatecall/)

---
## Level completed!

As the previous level, delegate mentions, the use of delegatecall to call libraries can be risky. This is particularly true for contract libraries that have their own state. This example demonstrates why the library keyword should be used for building libraries, as it prevents the libraries from storing and accessing state variables.



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



# 18) MagicNumber

Success condition:
> To solve this level, you only need to provide the Ethernaut with a Solver, a contract that responds to whatIsTheMeaningOfLife() with the right number.  
Easy right? Well... there's a catch.  
The solver's code needs to be really tiny. Really reaaaaaallly tiny. Like freakin' really really itty-bitty tiny: 10 opcodes at most.  
Hint: Perhaps its time to leave the comfort of the Solidity compiler momentarily, and build this one by hand O_o. That's right: Raw EVM bytecode.  
Good luck!  

Solidity is a high-level programming language that we need to compile to bytes so the EVM can undestand it. The bytecode gets executed as a number of opcodes.
There is two sets of opcodes: initialization opcodes which create the contract and store the second types of opcodes, runtime opcodes, which is the actual logic of your contract. It is the runtime opcodes that should be 10 opcodes at most.


## Runtimes opcodes
`PUSH1` = 0x60: push 1 byte on the stack
`MSTORE` = 0x52: store on the MEM
`RETURN` = 0xf3: return a value

We need to return the right number, i.e. [42](https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy#Answer_to_the_Ultimate_Question_of_Life,_the_Universe,_and_Everything_(42)). In order to return a value, we must first store that value (1) and then return it (2).
(1) Let's first store the return value (40 = 0x2a) in memory. We need to use the `MSTORE` opcode, the position we want to store the value (Let's take 0x00) and the value (0x2a).
    - We first `PUSH1` the value we want to store on the stack: push 0x2a -> 602a
    - Then `PUSH1` the place we want to store it: push 0x00 -> 6000
    - and finally the `MSTORE` opcode: mstore -> 52
    
We end up with 602a600052. That is 5 opcodes. We now need to return it.


(2) To return something, we need the `RETURN` opcode, the position of the return value and the size of the value. 
    - The size is 32 bytes (or 0x20 in hex): push 0x20 -> 6020
    - The position is 0x00: push 0x00 -> 6000
    - and the `RETURN` opcode: return -> f3

This second part give us 60206000f3. Another 5 opcodes. Putting both step together we get 602a60005260206000f3.


## Initialization opcodes

Now the initialization opcodes. We want to copy the runtime opcodes. 

The opcodes `CODECOPY` require 3 arguments the destination, the position of the code, and the size of the code. 
    - The size is 10 bytes: push 0x0a -> 600a
    - The position is 0x0c (the initialization opccodes will be 12 bytes in size): push 0x0c -> 600c
    - The destination is let's say 0x20: push 0x20 -> 6020
    - and the `CODECOPY` opcode: codecopy -> 39

Then we need to return the runtime opcodes so like above:
    - The size is 10 bytes: push 0x0a -> 600a
    - The position is 0x20: push 0x20 -> 6020
    - and the `RETURN` opcode: return -> f3

Our initialization opcodes is 600a600c602039600a6020f3

To get our final bytescode, we concat the two string: 0x600a600c602039600a6020f3602a60005260206000f3

---
Very detailed set of [articles](https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-i-introduction-832efd2d7737/) on the EVM.

### EVM opcodes

[List of opcodes](https://ethereum.org/en/developers/docs/evm/opcodes/)

### EVM



### Comparison

If we were to try to complet this challenge by writing a contract in solidity.

Writing a simple contract `SolverWayTooBig.sol` and using the compiler give us a bytecode:
6080604052348015600f57600080fd5b506004361060285760003560e01c806385bb7d6914602d575b600080fd5b60336049565b6040805160ff9092168252519081900360200190f35b602a9056fea26469706673582212208afe4970b1f40fb013ff56473b6e03c03f4fd7c05665e22589712f79a6aea1e764736f6c634300060c0033
with a size of 265, with opcodes:
"opcodes": "PUSH1 0x80 PUSH1 0x40 MSTORE CALLVALUE DUP1 ISZERO PUSH1 0xF JUMPI PUSH1 0x0 DUP1 REVERT JUMPDEST POP PUSH1 0x4 CALLDATASIZE LT PUSH1 0x28 JUMPI PUSH1 0x0 CALLDATALOAD PUSH1 0xE0 SHR DUP1 PUSH4 0x85BB7D69 EQ PUSH1 0x2D JUMPI JUMPDEST PUSH1 0x0 DUP1 REVERT JUMPDEST PUSH1 0x33 PUSH1 0x49 JUMP JUMPDEST PUSH1 0x40 DUP1 MLOAD PUSH1 0xFF SWAP1 SWAP3 AND DUP3 MSTORE MLOAD SWAP1 DUP2 SWAP1 SUB PUSH1 0x20 ADD SWAP1 RETURN JUMPDEST PUSH1 0x2A SWAP1 JUMP INVALID LOG2 PUSH5 0x6970667358 0x22 SLT KECCAK256 DUP11 INVALID 0x49 PUSH17 0xB1F40FB013FF56473B6E03C03F4FD7C056 PUSH6 0xE22589712F79 0xA6 0xAE LOG1 0xE7 PUSH5 0x736F6C6343 STOP MOD 0xC STOP CALLER ",
This is way too big to pass the level.



---
## Level completed!

Congratulations! If you solved this level, consider yourself a Master of the Universe.

Go ahead and pierce a random object in the room with your Magnum look. Now, try to move it from afar; Your telekinesis habilities might have just started working.



# 19) Alien Codex

Success condition:
> You've uncovered an Alien contract. Claim ownership to complete the level.

Once again, we need to claim ownership of a contract by changing the `owner` variable. Since our contract inherit `Ownable`, it will have an owner variable. This variable will be store in slot 0. AlienCodex variables are then store, since and address and a bool can share a 32 bytes slot, there are packed together so we end up with owner and bool in slot 0, followed by the dynamic array variable. the first available slot store the length of the dynamic array. The value of the array are store at address = keccak256(slot#) + (index * elementSize) => keccak256(1) + i.

Now let's talk about the vulnerability:
```
function retract() public contacted {
    codex.length--;
}
```
This function reduce the length of the array by 1. After initialization of the contract, the length is zero so calling this function will cause an underflow and set a new length of 2^256. This is the maximum amount of storage slot available to a contract and since the element of the array are of 32 bytes length, we can now access any slot of our contract storage and modify it with this function:
```
function revise(uint256 i, bytes32 _content) public contacted {
    codex[i] = _content;
}
```
So we just need to figure out which i corresponds to slot0 and we can change the owner of the contract. 
We know that at slot keccak(1) will be stored codex[0]
at slot keccak(1) + 1 will be stored codex[1]
at slot keccak(1) + i will be stored codex[i]
at slot 2^256 -1 will be stored codex[2^256 -1 -keccak(1)] and 
at slot 0 will be stored codex[2^256 -1 -keccak(1) +1]

So for i = 2^256 - keccak(1), and _content = our address, the `revise()` function will give us ownership of the contract. 

We can solve this level with a simple contract that will call the first two functions and then calculate the value of i we want to modify the owner variable:
```
function attack() public {
        AlienCodex(victim).make_contact();  // to pass the contacted modifier
        AlienCodex(victim).retract();  // create the underflow

        uint256 keccak_1 = uint256(keccak256(abi.encode(1)));
        uint256 i = 2**256 - 1 - keccak_1 + 1; // have to do -1 +1 to avoid TypeErrors
        AlienCodex(victim).revise(i, bytes32(uint256(msg.sender)));
    }
```

---

### Storage with inheritance
As we already saw, in solidity variable are store sequentially starting at slot 0 up to slot 2^256, packed together if possible in 32 bytes slot. When a contract inherit another, it also inherit its variables, and they are stored before the variable of the contract starting at the first contract inherited. The contract variables are then store in the following slots.

### Storage of dynamic type
For the type of a variable is dynamic, (e.g. dynamic array, mapping) the slot is use for the length of left empty and the value are store at addresses based on the keccak hash of the slot (keccak256(slot#) + (index * elementSize) for arrays, keccak256(key, slot#) for mappings))

---
## Level completed!

This level exploits the fact that the EVM doesn't validate an array's ABI-encoded length vs its actual payload.

Additionally, it exploits the arithmetic underflow of array length, by expanding the array's bounds to the entire storage area of 2^256. The user is then able to modify all contract storage.

Both vulnerabilities are inspired by 2017's [Underhanded coding contest](https://weka.medium.com/announcing-the-winners-of-the-first-underhanded-solidity-coding-contest-282563a87079)