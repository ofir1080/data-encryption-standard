
"""
Implementation of DES (Data Encryption Standard) algorithm,
one of the most famous algorithms for implementing symmetric cryptography in the world.

Modules:
BlockGenerator applies bitwise operations on the given message (64-bit size)
KeyGenerator generates 16 48-bit
MainFunc does the actual hashing with the message and the keys
Data the fixed data for implementing DES

Aouthor: Ofir Abramovich
"""

from modules import BlockGenerator, MainFunc, KeyGenerator
import Data


def hashIt(msg, initialKey, encrypt):
    """
    :param msg: 64-bit message
    :param initialKey: initial 64-bit key
    :param encrypt: if set to true do encryption otherwise decryption
    :return: 64-big encryption
    """
    keySet = KeyGenerator.create_key(initialKey)    # returns a list of 16 keys
    left, right = BlockGenerator.divide_left_right(msg)  # return the first divided block

    # sets direction of the loop according to encryption/decryption
    if encrypt is True:
        strt = 0
        fin = 16
        dir = 1
    else:
        strt = 15
        fin = -1
        dir = -1

    for i in range(strt, fin, dir):
        left, right = MainFunc.get_new_left_right(left, right, keySet[i + 1])

    reversed = (right << 32) | left  # 64 bit integer
    finalCrypt = 0
    for i, shifts in enumerate(Data.IPR):
        dig = reversed >> (64 - shifts) & 1
        finalCrypt |= dig << 63 - i
    return finalCrypt


# test for the message = 0x0321456789ABCDEF with key = 0x133457799BBCDFF1
msg = 0x0321456789ABCDEF
key = 0x133457799BBCDFF1
encr = hashIt(msg, key, True)
dcr = hashIt(encr, key, False)

print('{:<35s}{:>20s}{:>20s}{:>20s}'.format('The encrypted form of the message:', hex(msg)[2:], 'is: ', hex(encr)[2:]))
print('{:<35s}{:>20s}{:>20s}{:>20s}'.format('The decrypted form of the hash:', hex(encr)[2:], 'is: ', hex(dcr)[2:]))