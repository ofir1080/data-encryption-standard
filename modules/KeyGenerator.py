"""
All key-generator functions
"""
import Data

def divide_key_into_bytes(fullKey):
    """
    divide key into bytes.
    :param fullKey: 64-bit initial key
    :return: list of 1-byte sub keys
    """
    subKeys = []
    for i in range(7, -1, -1):
        subKeys.append((fullKey & (0xFF << 8 * i)) >> 8 * i)
    return subKeys


def permute_key(key):
    """
    generates 56-bit key using the mapping PC1 table.
    :param key: 64-bit initial key
    :return: 56-bit length new permuted key
    """


    permutedKey = 0
    for i in range(len(Data.PC1)):
        bit = (key >> 64 - Data.PC1[i]) & 1
        permutedKey |= (bit << 55 - i)
    return permutedKey


def divide_permuted_key(permuted):
    """
    divides 56-bit key into left and right (28-but each).
    :param permuted: 56-bit permuted key
    :return: splitted into 2 keys
    """
    left = (permuted & 0xFFFFFFF0000000) >> 28
    right = permuted & 0xFFFFFFF
    return left, right


def bit_left_rotate(zero):
    """
    generates 16 28-bit sub keys out of either left/right splitted kyes.
    :param zero: the 0th left/right 28-bit key
    :return: number-of-left-shifts list
    """

    keyList = [zero]
    for i in range(16):
        for j in range(Data.schedule[i]):
            leftBit = (0x8000000 & zero) >> 27
            rotated = leftBit | (zero << 1)
            normalized = rotated & 0xFFFFFFF

            zero = normalized
        keyList.append(normalized)
    return keyList


def merge_and_permute(left, right):
    """
    merges left and right subkeys (as leftright) and permutes 16 48 keys long
    :param left: 16 left keys
    :param right: 16 right keys
    :return: a list of 16 final keys
    """

    keys48 = [-1]  # normalize indexes
    for key in range(1, 17):
        concat = (left[key] << 28) | right[key]
        # test = bin(concat)[2:].zfill(56)
        key48 = 0
        for i, j in enumerate(Data.PC2):
            bit = (concat >> 56 - j) & 1
            key48 |= (bit << 48 - i - 1)
        keys48.append(key48)
    return keys48


def create_key(initalKey):

    permuted = permute_key(initalKey)
    # print('permuted key:', len(bin(permuted)[2:]))

    c_0 = divide_permuted_key(permuted)[0]
    d_0 = divide_permuted_key(permuted)[1]

    leftKeys = bit_left_rotate(c_0)
    rightKeys = bit_left_rotate(d_0)

    keys48 = merge_and_permute(leftKeys, rightKeys)

    # for i, key in enumerate(keys48):
    #     print('KEY ', i, ':\t', bin(key)[2:].zfill(48))

    return merge_and_permute(leftKeys, rightKeys)


# create_key(1383827165325090801) # test