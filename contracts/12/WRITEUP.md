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