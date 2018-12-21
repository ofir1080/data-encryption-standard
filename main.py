



def divideHalf(block):
    # block = block[2:].zfill(64)

    left = (block & 0xFFFFFFFF00000000) >> 32
    right = block & 0x00000000FFFFFFFF
    return left, right



plainTextBlock = 0x0123456789ABCDEF
print('plain text block:', plainTextBlock)
left, right = divideHalf(plainTextBlock)
print('left: ', left, 'right: ',right)