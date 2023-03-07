// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;


import "./challange.sol";

contract exp {
    function attack(address challangeAddress) public {
        Challange challangeContract = Challange(challangeAddress);
        challangeContract.getFlag();
    }
}