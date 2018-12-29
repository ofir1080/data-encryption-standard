import BlockGenerator
import KeyGenerator
import Data


def expand_right_to48(right):
    """
    expands the right block of text block to 48 bits (instead of 32)
    :param right: 32-bit right block of text
    :return: expanded right block
    """

    expanded = 0
    for i, num in enumerate(Data.E):
        bit = (right >> 32 - num) & 1
        expanded |= (bit << 48 - i - 1)
    return expanded


def xor_key(right, key):
    return right ^ key


def divide_into_8_blocks(xored):
    """
    devides the right block XORed with the key into 8 block s of 6 bits
    :param xored: right XOR key
    :return: list of 8 6-bit
    """
    blockList = []
    for i in range(7, -1, -1):
        blockList.append(xored >> i*6 & 0b111111)

    # test
    # for num in blockList:
    #     print(bin(num)[2:].zfill(6))
    return blockList


def permute_into_4(origin, table):
    """
    permutes 6-bit sub-block into 4 using the mapping table
    :param origin: 6-bit integer
    :param dest: mapping table
    :return: new 4-bit permuted sub-block
    """
    rowNum = ((origin & 0b100000) >> 4) + (origin & 0b000001)
    colNum = (origin & 0b011110) >> 1
    return table[rowNum][colNum]


def turn_48_into_32(dividedBlock):
    """
    :param divided: a list of 8 6-bit integers
    :return: 32-bit integer
    """
    res = 0
    for i in range(8):
        fourBit = permute_into_4(dividedBlock[i], Data.sBox[i])
        # print(bin(fourBit)[2:].zfill(4))
        res += (fourBit << (7 - i)*4)
    # print(bin(res)[2:].zfill(32))
    return res


def final_permute(num):
    """
    final permutation according to the mapping table P
    :param num: 32-bit integer
    :return: permuted 32-bit integer
    """
    f = 0
    for i, shifts in enumerate(Data.P):
        dig = num >> (32 - shifts) & 1
        f |= dig << 31 - i
    # print(bin(f)[2:].zfill(32))
    return f


def get_new_left_right(left, right, key):

    newLeft = right

    # generates the new right block applying f
    expanded48 = expand_right_to48(right)
    keyXorRight = xor_key(expanded48, key)
    divided = divide_into_8_blocks(keyXorRight)
    permuted = turn_48_into_32(divided)
    f = final_permute(permuted)
    newRight = f ^ left

    return newLeft, newRight

# tests

# key = KeyGenerator.create_key(0x133457799BBCDFF1)[1]
# left, right = BlockGenerator.divide_left_right(0x0123456789ABCDEF)
#
# newLeft, newRight = get_new_left_right(left, right, key)
#
# print(bin(newRight)[2:].zfill(32))





