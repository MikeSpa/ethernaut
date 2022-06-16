// SPDX-License-Identifier: MIT
pragma solidity <0.7.0;

contract MotorbikeAttack {}

contract SeflDestructContract {
    function destruct() public {
        selfdestruct(address(0));
    }
}
