// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./DoubleEntryPoint.sol";

contract DetectionBot is IDetectionBot {
    Forta public forta;

    constructor(address _forta) public {
        forta = Forta(_forta);
    }

    function handleTransaction(address _user, bytes calldata _msgData)
        external
        override
    {
        // get the signature of the function in _msgData
        bytes4 signature = bytes4(_msgData[0]) |
            (bytes4(_msgData[1]) >> 8) |
            (bytes4(_msgData[2]) >> 16) |
            (bytes4(_msgData[3]) >> 24);

        //compare it with the delegateTransfer signature
        if (
            signature ==
            bytes4(
                keccak256(
                    abi.encodePacked(
                        "delegateTransfer(address,uint256,address)"
                    )
                )
            )
        ) {
            forta.raiseAlert(_user); // if its the same raise an alert
        }
    }
}
