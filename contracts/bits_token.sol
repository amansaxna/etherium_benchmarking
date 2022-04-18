// SPDX-License-Identifier: MIT

pragma solidity 0.4.22;
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
contract tokenRecipient { function receiveApproval(address _from, uint256 _value, address
_token, bytes _extraData); }
contract token {
 /* Public variables of the token */
 string public standard = 'Token 0.1';
 string public name;
 string public symbol;
 uint8 public decimals;
 uint256 public totalSupply;
 /* This creates an array with all balances */
 mapping (address => uint256) public balanceOf;
 mapping (address => mapping (address => uint256)) public allowance;
 /* This generates a public event on the blockchain that will notify clients */
 event Transfer(address indexed from, address indexed to, uint256 value);
 /* Initializes contract with initial supply tokens to the creator of the contract */
 function token(
 uint256 initialSupply,
 string tokenName,
 uint8 decimalUnits,
 string tokenSymbol
 ) {
 balanceOf[msg.sender] = initialSupply; // Give the creator all initial tokens (by default it has to be greater that 0)
 totalSupply = initialSupply; // Update total supply
 name = tokenName; // Set the name for display purposes
 symbol = tokenSymbol; // Set the symbol for display purposes
 decimals = decimalUnits; // Amount of decimals for display purposes
 }
 /* Send coins */
 function transfer(address _to, uint256 _value) {
 if (balanceOf[msg.sender] < _value) throw; // Check if the sender has enough
 if (balanceOf[_to] + _value < balanceOf[_to]) throw; // Check for overflows
 balanceOf[msg.sender] -= _value; // Subtract from the sender
 balanceOf[_to] += _value; // Add the same to the recipient
 Transfer(msg.sender, _to, _value); // Notify anyone listening that this transfer tookplace
 }
 /* This unnamed function is called whenever someone tries to send ether to it */
 /*
 function () {
 throw; // Prevents accidental sending of ether
 }
 */
}
//******************************************************************************
//*****************************************************************************
//******************************************************************************
contract MyAdvancedToken is owned, token {
 mapping (address => bool) public frozenAccount;
 mapping (uint => address) public findUserStep1;
 mapping (address => string) public findUserStep2;
 mapping (uint => string) public findUserEC;
 mapping (address => uint) public penaltyCount;

 uint public count;
 uint public countEC;
 /* This generates a public event on the blockchain that will notify clients */
 event FrozenFunds(address target, bool frozen);
 /* Initializes contract with initial supply tokens to the creator of the contract */
 function MyAdvancedToken(
 uint256 initialSupply,
 string tokenName,
 uint8 decimalUnits,
 string tokenSymbol
 ) token (initialSupply, tokenName, decimalUnits, tokenSymbol) {}
 /* Send coins */
 function transfer(address _to, uint256 _value) {
 if (balanceOf[msg.sender] < _value) throw; // Check if the sender has enough
 if (balanceOf[_to] + _value < balanceOf[_to]) throw; // Check for overflows
 if (frozenAccount[msg.sender]) throw; // Check if frozen
 balanceOf[msg.sender] -= _value; // Subtract from the sender
 balanceOf[_to] += _value; // Add the same to the recipient
 Transfer(msg.sender, _to, _value); // Notify anyone listening that this transfer took place
 }
 /* A contract attempts to get the coins */
 function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
 if (frozenAccount[_from]) throw; // Check if frozen
 if (balanceOf[_from] < _value) throw; // Check if the sender has enough
 if (balanceOf[_to] + _value < balanceOf[_to]) throw; // Check for overflows
 if (_value > allowance[_from][msg.sender]) throw; // Check allowance
 balanceOf[_from] -= _value; // Subtract from the sender
 balanceOf[_to] += _value; // Add the same to the recipient
 allowance[_from][msg.sender] -= _value;
 Transfer(_from, _to, _value);
 return true;
 }

 function smartUsersPayments(address _user, uint256 _origin) payable onlyOwner returns (bool
success) {
 if (_user == 0x0) throw;
if (balanceOf[msg.sender] < 10) throw;
 if (balanceOf[_user] + 10 < balanceOf[_user]) throw;

 uint mintedAmount = 10;
 uint aux =0;
 uint positivePoints = 2;
 uint negativePoints = 5;
 uint destroyAmount = 5;
 if((_origin>0) && (_origin<= 100)){

 //the minning of this token are the good actions of the people
 balanceOf[_user] += mintedAmount; // user gets 10 token for good action
 totalSupply += mintedAmount; //total supply increases in 10
 Transfer(0, this, mintedAmount);
 Transfer(this, _user, mintedAmount);

 aux = penaltyCount[_user]; //get the penalty count from the user
 if (penaltyCount[_user] == 1){
 penaltyCount[_user] = 0; //update the penalty number to 0
 }
 if (penaltyCount[_user] > positivePoints){
 penaltyCount[_user] = aux -positivePoints; //update the penalty number -2
 }
 // unfreeze account if point go lower than 25
 if (penaltyCount[_user] < 25){
 frozenAccount[_user] = false;
 FrozenFunds(_user, false);
 }
 return true;
 }
 else{
 //to prevent inflation everey bad action will destroy 5 coins from the total supply
 //this tokens are destroyed from the user account
 if(balanceOf[_user] >= destroyAmount){
 balanceOf[_user] -= destroyAmount; // user destroys 5 token for bad action
 totalSupply -= destroyAmount; //total supply decreases in 5
 //Transfer(0, this, mintedAmount);
 //Transfer(this, _user, mintedAmount);
 } else {
 if((balanceOf[_user] > 0) && (balanceOf[_user] < destroyAmount)){
 uint aux2 = balanceOf[_user];
 balanceOf[_user]-= aux2; //balance of the user gets to 0
 totalSupply -= aux2;
 }
 }
 aux = penaltyCount[_user]; //get the penalty count from the user
 penaltyCount[_user] = aux + negativePoints; //update the penalty number +5
 // 25 penalty point equals facount frozen
 if (penaltyCount[_user] >= 25){
 frozenAccount[_user] = true;
 FrozenFunds(_user, true);
 }
 }
 }
 //******************************
 //******ADD USER FUNCITON ******
 function addUser(address publicKey, string id) onlyOwner {
 findUserStep1[count] = publicKey;
 findUserStep2[publicKey] = id;
 penaltyCount[publicKey] = 0; //initialize penalty in 0
 count++;
 }
 function addUserEC(uint idEC, string id) onlyOwner {
 findUserEC[idEC] = id;
 countEC++;
 }
}