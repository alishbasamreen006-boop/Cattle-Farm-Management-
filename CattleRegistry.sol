// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title CattleRegistry
/// @notice Stores tamper-proof fingerprints (hashes) of cattle farm events.
/// Detailed data stays in the normal database; only the hash goes on-chain.
contract CattleRegistry {
    struct Event {
        string eventType;   // REGISTRATION, VACCINATION, TREATMENT, SALE ...
        bytes32 dataHash;   // SHA-256 fingerprint of the record
        address recordedBy; // wallet that saved it
        uint256 timestamp;  // block time
    }

    mapping(string => Event[]) private history; // animal tag => events

    event EventRecorded(string animalTag, string eventType, bytes32 dataHash, address recordedBy);

    function addEvent(string calldata animalTag, string calldata eventType, bytes32 dataHash) external {
        history[animalTag].push(Event(eventType, dataHash, msg.sender, block.timestamp));
        emit EventRecorded(animalTag, eventType, dataHash, msg.sender);
    }

    function eventCount(string calldata animalTag) external view returns (uint256) {
        return history[animalTag].length;
    }

    function getEvent(string calldata animalTag, uint256 index)
        external view returns (string memory, bytes32, address, uint256)
    {
        Event storage e = history[animalTag][index];
        return (e.eventType, e.dataHash, e.recordedBy, e.timestamp);
    }
}
