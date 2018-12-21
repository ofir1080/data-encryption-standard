
"""
All key-generator functions
"""



def divideKeyIntoBytes(fullKey):
    subKeys = []
    for i in range(7, -1 , -1):
        subKeys.append((fullKey & (0xFF << 8 * i)) >> 8 * i)
    return subKeys


def permuteKey(key, PC1):
    permutedKey = 0
    for i in range(len(PC1)):
        bit = (key >> 64 - PC1[i]) & 1
        permutedKey |= (bit << 55 - i)
    return permutedKey


def dividePermutedKey(permuted):

    left = (permuted & 0xFFFFFFF0000000) >> 28
    right = permuted & 0x0000000FFFFFFFF
    return left, right

def bitLeftRoatate(key):
    leftBit = (0x8000000 & key) >> 27
    rotated = leftBit | (key << 1)
    return rotated & 0xFFFFFFF



def main():

    # key = 0x133457799BBCDFF1
    # subKeys = divideKeyIntoBytes(key)
    # print('8-bit devided key:', subKeys)

    PC1 = [57, 49, 41, 33, 25, 17, 9, 1,
           58, 50, 42, 34, 26, 18, 10, 2,
           59, 51, 43, 35, 27, 19, 11, 3,
           60, 52, 44, 36, 63, 55, 47, 39,
           31, 23, 15, 7, 62, 54, 46, 38,
           30, 22, 14, 6, 61, 53, 45, 37,
           29, 21, 13, 5, 28, 20, 12, 4]

    key = 0x133457799BBCDFF1
    permuted = permuteKey(key, PC1)
    print('permuted key:', len(bin(permuted)[2:]))

    c_0 = dividePermutedKey(permuted)[0]
    d_0 = dividePermutedKey(permuted)[1]
    print('C0: ', bin(c_0).zfill(28)[2:], ' D0: ', bin(d_0).zfill(28)[2:])

    cNext = bitLeftRoatate(c_0)
    for i in range (160):
        print('Cn+1: ', bin(cNext)[2:].zfill(28))
        cNext = bitLeftRoatate(cNext)


main()