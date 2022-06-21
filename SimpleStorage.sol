//SPDX-License-Identifier:MIT

pragma solidity ^0.8.10;

contract SimpleStorage {
    uint256 public favNumber;
    struct Person {
        string name;
        uint256 amount;
    }

    Person[] public balance;
    mapping(string => uint256) public nameToNumber;

    function add_person(string memory _name, uint256 _amount) public {
        balance.push(Person({name: _name, amount: _amount}));
        nameToNumber[_name] = _amount;
    }

    uint256[] public sample;

    function push_numbers(uint256 no) public {
        sample.push(no);
    }

    function store(uint256 _fav) public {
        favNumber = _fav;
    }

    function retrieve() public view returns (uint256) {
        return favNumber;
    }
}
