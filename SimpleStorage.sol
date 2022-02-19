// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract SimpleStorage {
    uint256 favouriteNumber = 5;
    struct People  {
    string name;
        uint256 favouriteNumber;
    }
    People[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;

    function store(uint256 _favouriteNumber) public {
    favouriteNumber = _favouriteNumber;
    }
    function retrieve() public view returns(uint256) {
        return favouriteNumber;
    }
    function addPerson(string memory name, uint256 _favouriteNumber) public{
        people.push(People({name: name, favouriteNumber: _favouriteNumber}));
        nameToFavouriteNumber[name] = _favouriteNumber;
    }
 
}