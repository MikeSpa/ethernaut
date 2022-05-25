# 21) Shop

Success condition:
> Сan you get the item from the shop for less than the price asked?

This level is similar to the Elevator one, where you the level contract calls an external function and you need to give two different answers. Here the function that gets called is `price()`. 

The difference here is that the function called must be a view meaning it cannot change the state of the variable. We have to find another way to give a different answer the second time the function is called. The only thing that chage between the two call is the `isSold` variable in the Shop contract. We can use it to give a different answer.
With a simple terniary operator: ```Shop(victim).isSold() ? 1 : 100;```


---
### View function
View function cannot modify the state of the contract, The following statements are considered modifying the state:

- Writing to state variables.
- Emitting events.
- Creating other contracts.
- Using selfdestruct.
- Sending Ether via calls.
- Calling any function not marked view or pure.
- Using low-level calls.
- Using inline assembly that contains certain opcodes.

---
## Level completed!

Contracts can manipulate data seen by other contracts in any way they want.

It's unsafe to change the state based on external and untrusted contracts logic.
