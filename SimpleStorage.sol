// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.9.0;

// Class
contract SimpleStorage {
    // It will be compiled by the EVM (Eth Virtual Machine).
    // Will also work with other blockchains

    // This will be initialized to 0!
    // internal is the default
    // type visibility name
    uint256 internal favoriteNumber;

    // structs define new types in solidity
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // Dynamic Array
    People[] public people;

    // mapping: data structure
    // mapping is a dictionary like data structure with 1 value per key
    mapping(string => uint256) public nameToFavoriteNumber;

    // Fixed Array: People[1]
    // Function
    // Calling a function costs gas because fucntion call is also a transaction. Changing a state is also a transaction
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view, pure
    // view -> reading state of a blockchain
    // public varialbes are automatically view function
    // pure -> purely do some type of math
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // two ways to store: memory or storage
    // memory -> only be stored during execution of the call
    // storage -> will persist even after execution
    // strings are not value type. They are objects. An array of bytes.
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
