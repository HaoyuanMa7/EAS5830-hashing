#!/bin/python
import hashlib
import os
import random


def mine_block(k, prev_hash, transactions):
    """
        k - Number of trailing zeros in the binary representation (integer)
        prev_hash - the hash of the previous block (bytes)
        rand_lines - a set of "transactions," i.e., data to be included in this block (list of strings)

        Complete this function to find a nonce such that 
        sha256( prev_hash + rand_lines + nonce )
        has k trailing zeros in its *binary* representation
    """
    if not isinstance(k, int) or k < 0:
        print("mine_block expects positive integer")
        return b'\x00'

    # TODO your code to find a nonce here
    nonce_counter = 0
    
    # Create a mask for checking k trailing zeros in binary
    # For k trailing zeros, the last k bits should be 0
    # So hash_value & ((1 << k) - 1) should equal 0
    mask = (1 << k) - 1
    
    while True:
        # Create the nonce as bytes
        nonce = str(nonce_counter).encode('utf-8')
        
        # Create the hash object
        m = hashlib.sha256()
        
        # Add previous block hash
        m.update(prev_hash)
        
        # Add all transactions in order
        for transaction in transactions:
            m.update(transaction.encode('utf-8'))
        
        # Add the nonce
        m.update(nonce)
        
        # Get the hash digest as bytes
        hash_bytes = m.digest()
        
        # Convert hash bytes to integer for checking trailing zeros
        hash_int = int.from_bytes(hash_bytes, byteorder='big')
        
        # Check if the last k bits are all zeros
        if (hash_int & mask) == 0:
            # Found a valid nonce
            break
        
        nonce_counter += 1

    assert isinstance(nonce, bytes), 'nonce should be of type bytes'
    return nonce


def get_random_lines(filename, quantity):
    """
    This is a helper function to get the quantity of lines ("transactions")
    as a list from the filename given. 
    Do not modify this function
    """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())

    random_lines = []
    for x in range(quantity):
        random_lines.append(lines[random.randint(0, quantity - 1)])
    return random_lines


if __name__ == '__main__':
    # This code will be helpful for your testing
    filename = "bitcoin_text.txt"
    num_lines = 10  # The number of "transactions" included in the block

    # The "difficulty" level. For our blocks this is the number of Least Significant Bits
    # that are 0s. For example, if diff = 5 then the last 5 bits of a valid block hash would be zeros
    # The grader will not exceed 20 bits of "difficulty" because larger values take to long
    diff = 20

    # Create a dummy previous hash (genesis block)
    prev_hash = b'\x00' * 32  # 32 bytes of zeros for genesis block
    
    transactions = get_random_lines(filename, num_lines)
    nonce = mine_block(diff, prev_hash, transactions)
    print(nonce)
