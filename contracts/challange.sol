// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

contract Challange {
    event SendFlag();

    function getFlag() public {
        emit SendFlag();
    }
}
