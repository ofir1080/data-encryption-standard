"""
All key-generator functions
"""


def divideKeyIntoBytes(fullKey):
    """
    divide key into bytes.
    :param fullKey: 64-bit initial key
    :return: list of 1-byte sub keys
    """
    subKeys = []
    for i in range(7, -1, -1):
        subKeys.append((fullKey & (0xFF << 8 * i)) >> 8 * i)
    return subKeys


def permuteKey(key):
    """
    generates 56-bit key using the mapping PC1 table.
    :param key: 64-bit initial key
    :return: 56-bit length new permuted key
    """
    PC1 = [57, 49, 41, 33, 25, 17, 9, 1,
           58, 50, 42, 34, 26, 18, 10, 2,
           59, 51, 43, 35, 27, 19, 11, 3,
           60, 52, 44, 36, 63, 55, 47, 39,
           31, 23, 15, 7, 62, 54, 46, 38,
           30, 22, 14, 6, 61, 53, 45, 37,
           29, 21, 13, 5, 28, 20, 12, 4]

    permutedKey = 0
    for i in range(len(PC1)):
        bit = (key >> 64 - PC1[i]) & 1
        permutedKey |= (bit << 55 - i)
    return permutedKey


def dividePermutedKey(permuted):
    """
    divides 56-bit key into left and right (28-but each).
    :param permuted: 56-bit permuted key
    :return: splitted into 2 keys
    """
    left = (permuted & 0xFFFFFFF0000000) >> 28
    right = permuted & 0xFFFFFFF
    return left, right


def bitLeftRoatate(zero):
    """
    generates 16 28-bit sub keys out of either left/right splitted kyes.
    :param zero: the 0th left/right 28-bit key
    :return: number-of-left-shifts list
    """
    schedule = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    keyList = [zero]
    for i in range(16):
        for j in range(schedule[i]):
            leftBit = (0x8000000 & zero) >> 27
            rotated = leftBit | (zero << 1)
            normalized = rotated & 0xFFFFFFF

            zero = normalized
        keyList.append(normalized)
    return keyList


def mergeAndPermute(left, right):
    """
    merges left and right subkeys (as leftright) and permutes 16 48 keys long
    :param left: 16 left keys
    :param right: 16 right keys
    :return: a list of 16 final keys
    """

    PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
           15, 6, 21, 10, 23, 19, 12, 4,
           26, 8, 16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55, 30, 40,
           51, 45, 33, 48, 44, 49, 39, 56,
           34, 53, 46, 42, 50, 36, 29, 32]

    keys48 = [-1]  # normalize indexes
    for key in range(1, 17):
        concat = (left[key] << 28) | right[key]
        test = bin(concat)[2:].zfill(56)
        key48 = 0
        for i, j in enumerate(PC2):
            bit = (concat >> 56 - j) & 1
            key48 |= (bit << 48 - i - 1)
        keys48.append(key48)
    return keys48


def createKey(inital_key):

    permuted = permuteKey(inital_key)
    print('permuted key:', len(bin(permuted)[2:]))

    c_0 = dividePermutedKey(permuted)[0]
    d_0 = dividePermutedKey(permuted)[1]
    print('C0: ', bin(c_0).zfill(28)[2:], '\nD0: ', bin(d_0)[2:].zfill(28))

    leftKeys = bitLeftRoatate(c_0)
    for i, key in enumerate(leftKeys):
        print('Cx:', i, '\t', bin(key)[2:].zfill(28))

    rightKeys = bitLeftRoatate(d_0)

    keys48 = mergeAndPermute(leftKeys, rightKeys)

    for i, key in enumerate(keys48):
        print('KEY ', i, ':\t', bin(key)[2:].zfill(48))

    return mergeAndPermute(leftKeys, rightKeys)


# createKey(0x133457799BBCDFF1) # test