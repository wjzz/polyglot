import sys

"""
NOTE: 
Only the memory consumption directly attributed to the object is accounted for, 
not the memory consumption of objects it refers to.

Recipe for recursive sizeof:
https://code.activestate.com/recipes/577504/
"""

def getsizeof_list(l):
    basic = sys.getsizeof(l)
    return basic + sum(sys.getsizeof(elem) for elem in l)

print("sizeof of various python's std data structures (in bytes):")

print("empty string = ", sys.getsizeof(""))
print("single ascii char string = ", sys.getsizeof("a"))
print("single hiragana char string = ", sys.getsizeof("か"))
print("single kanji char string = ", sys.getsizeof("人"))

# seems to be 24 + 4 bytes every 2^32
for num in [0, 1, 2, 256, 10 ** 6, 10 ** 9, 10 ** 12, 10 ** 15]:
    print(f"num = {num:21,} has size {sys.getsizeof(num)} bytes")

# seems to be 64 bytes + 8 bytes for each additional element
for l in [[], [1], [1,2], list(range(10))]:
    print(f"l = {l!r} has shallow size {sys.getsizeof(l)} bytes")

for l in [[], [1], [1,2], list(range(10))]:
    print(f"l = {l!r} has total size {getsizeof_list(l)} bytes")

# OUTPUT:

# wjzz:~/prog/polyglot/sizeof/python$ p mem_size_ex.py 
# sizeof of various python's std data structures (in bytes):
# empty string =  49
# single ascii char string =  50
# single hiragana char string =  76
# single kanji char string =  76
# num =                     0 has size 24 bytes
# num =                     1 has size 28 bytes
# num =                     2 has size 28 bytes
# num =                   256 has size 28 bytes
# num =             1,000,000 has size 28 bytes
# num =         1,000,000,000 has size 28 bytes
# num =     1,000,000,000,000 has size 32 bytes
# num = 1,000,000,000,000,000 has size 32 bytes
# l = [] has shallow size 64 bytes
# l = [1] has shallow size 72 bytes
# l = [1, 2] has shallow size 80 bytes
# l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] has shallow size 200 bytes
# l = [] has total size 64 bytes
# l = [1] has total size 100 bytes
# l = [1, 2] has total size 136 bytes
# l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] has total size 476 bytes
