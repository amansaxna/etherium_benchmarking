pragma solidity 0.4.11;
contract owned {
 address public owner;
 function owned() {
 owner = msg.sender;
 }
 modifier onlyOwner {
 if (msg.sender != owner) throw;
 _;
 }
}