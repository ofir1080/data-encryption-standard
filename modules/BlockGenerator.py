
import Data

def initialPermute(block):
    """
    permutes a single block according to the given map
    :param block: a plaintext block of data
    :return: the permuted block
    """
    ip = 0
    for i, num in enumerate(Data.permuteMap):
        bit = (block >> 64 - num) & 1
        ip |= (bit << 64 - i - 1)
    return ip

def divideHalf(block):

    left = (block & 0xFFFFFFFF00000000) >> 32
    right = block & 0x00000000FFFFFFFF
    return left, right


def divide_left_right(blockMsg):
    """
    returns 'left' & 'right' block elements
    :param block: initial block
    :return:
    """
    ip = initialPermute(blockMsg)
    left, right = divideHalf(ip)

    return left, right

# divide_left_right(4037734570)