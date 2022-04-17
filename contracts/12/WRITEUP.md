# 12) Privacy

Success condition:
> The creator of this contract was careful enough to protect the sensitive areas of its storage.  
Unlock this contract to beat the level.

Just like for the 8th level, we need to find out what is written in a variable to unlock the contract. Since the variable is priavate we can't access it via a getter. We need to figure out where is the storage slot the key is and retrieve it with GetStorageAt. Smart contract storage have 2^256 32bytes slots. it two consecutive variable can fit in one slot they are packed together from right to left.

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