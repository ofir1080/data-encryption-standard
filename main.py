import BlockGenerator
import KeyGenerator


def hashing(right, key):

    E = [32, 1, 2, 3, 4, 5, 4, 5,
          6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16,
         17, 16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25, 24,
         25, 26, 27, 28, 29, 28, 29,
         30, 31, 32, 1]

    expanded = 0
    for i, num in enumerate(E):
        bit = (right >> 32 - num) & 1
        expanded |= (bit << 48 - i - 1)
    return expanded;


# keys = KeyGenerator.createKey(0x133457799BBCDFF1)   # 64-bit initial key
# left, right = BlockGenerator(81985529216486895)

test = 4037734570
res = hashing(test, 0)
print(bin(res)[2:].zfill(48))

# for i in range(1, 17):
#     newLeft = right
#     newRight = left ^ hashing(right, keys[i])