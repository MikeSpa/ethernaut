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
### nothing

---
## Level completed

nothing much