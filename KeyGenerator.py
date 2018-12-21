
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
    for i in range(7, -1 , -1):
        subKeys.append((fullKey & (0xFF << 8 * i)) >> 8 * i)
    return subKeys


def permuteKey(key, PC1):
    """
    generates 56-bit key using the mapping PC1 table.
    :param key: 64-bit initial key
    :param PC1: the mapping table
    :return: 56-bit length new permuted key
    """
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

def bitLeftRoatate(zero, schedule):
    """
    generates 16 28-bit sub keys out of either left/right splitted kyes.
    :param zero: the 0th left/right 28-bit key
    :param schedule:
    :return: number-of-left-shifts list
    """
    keyList = []
    for i in range (16):
        for j in range(schedule[i]):
            leftBit = (0x8000000 & zero) >> 27
            rotated = leftBit | (zero << 1)
            normalized = rotated & 0xFFFFFFF

            zero = normalized
        keyList.append(normalized)
    return keyList




def main():



    # constants
    key = 0x133457799BBCDFF1

    PC1 = [57, 49, 41, 33, 25, 17, 9, 1,
           58, 50, 42, 34, 26, 18, 10, 2,
           59, 51, 43, 35, 27, 19, 11, 3,
           60, 52, 44, 36, 63, 55, 47, 39,
           31, 23, 15, 7, 62, 54, 46, 38,
           30, 22, 14, 6, 61, 53, 45, 37,
           29, 21, 13, 5, 28, 20, 12, 4]

    scheduleLeftShifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
           15, 6, 21, 10, 23, 19, 12, 4,
           26, 8, 16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55, 30, 40,
           51, 45, 33, 48, 44, 49, 39, 56,
           34, 53, 46, 42, 50, 36, 29, 32]


    #tests
    permuted = permuteKey(key, PC1)
    print('permuted key:', len(bin(permuted)[2:]))

    c_0 = dividePermutedKey(permuted)[0]
    d_0 = dividePermutedKey(permuted)[1]
    print('C0: ', bin(c_0).zfill(28)[2:], '\nD0: ', bin(d_0)[2:].zfill(28))

    leftKeys = bitLeftRoatate(c_0, scheduleLeftShifts)
    for i, key in enumerate(leftKeys):
        print('Cx:', i + 1, '\t', bin(key)[2:].zfill(28))


    rightKeys = bitLeftRoatate(d_0, scheduleLeftShifts)
    for i, key in enumerate(rightKeys):
        print('Dx:', i + 1, '\t', bin(key)[2:].zfill(28))



main()