
"""
All key-generator functions
"""


def divideHalf(block):
    # block = block[2:].zfill(64)

    left = (block & 0xFFFFFFFF00000000) >> 32
    right = block & 0x00000000FFFFFFFF
    return left, right


def devideKeyIntoBytes(fullKey):
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


def main():
    plainTextBlock = 0x0123456789ABCDEF
    print('plain text block:', plainTextBlock)
    left, right = divideHalf(plainTextBlock)
    print('left: ', left, 'right: ',right)

    key = 0x133457799BBCDFF1
    subKeys = devideKeyIntoBytes(key)
    print('8-bit devided key:', subKeys)

    PC1 = [57, 49, 41, 33, 25, 17, 9, 1,
           58, 50, 42, 34, 26, 18, 10, 2,
           59, 51, 43, 35, 27, 19, 11, 3,
           60, 52, 44, 36, 63, 55, 47, 39,
           31, 23, 15, 7, 62, 54, 46, 38,
           30, 22, 14, 6, 61, 53, 45, 37,
           29, 21, 13, 5, 28, 20, 12, 4]

    key = 0x133457799BBCDFF1
    print('permuted key:', permuteKey(0x133457799BBCDFF1, PC1))

main()