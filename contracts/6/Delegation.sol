// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Delegate {
    address public owner;

    constructor(address _owner) public {
        owner = _owner;
    }

    function pwn() public {
        owner = msg.sender;
    }
}

contract Delegation {
    //Since Delegate::pwn() modify the first slot of its storage
    // if Delegation has another variable declare first, that one would be modify instead of owner
    // address public other_variable;
    address public owner;
    Delegate delegate;

    constructor(address _delegateAddress) public {
        delegate = Delegate(_delegateAddress);
        owner = msg.sender;
    }

    fallback() external {
        (bool result, ) = address(delegate).delegatecall(msg.data);
        if (result) {
            this;
        }
    }
}
