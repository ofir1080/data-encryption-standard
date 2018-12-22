
def initialPermute(block):
    """
    permutes a single block according to the given map
    :param block: a plaintext block of data
    :return: the permuted block
    """

    permuteMap = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]
    ip = 0
    for i, num in enumerate(permuteMap):
        bit = (block >> 64 - num) & 1
        ip |= (bit << 64 - i - 1)
    return ip

def divideHalf(block):

    left = (block & 0xFFFFFFFF00000000) >> 32
    right = block & 0x00000000FFFFFFFF
    return left, right


def getBoock(block):
    """
    returns 'left' & 'right' block elements
    :param block: initial block
    :return:
    """

    test = 81985529216486895
    ip = initialPermute(test)
    print(bin(ip)[2:].zfill(64))

    left, right = divideHalf(ip)
    print(bin(left)[2:].zfill(32), '\t', bin(right)[2:].zfill(32))

    return left, right