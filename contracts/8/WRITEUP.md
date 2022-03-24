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
