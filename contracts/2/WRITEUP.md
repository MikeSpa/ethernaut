# 2 Fallout

Here again, we simply need to take ownership of the contract. We can see that the "constructor" function is actually a regular function and thus callable by anyone. Calling it will change the `owner` to `msg.sender` and we are already done:

> ```contract.Fal1out()```
