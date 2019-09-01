# for this version 35 is close to the limit
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

# this is still slow as it only performs shallow memoization
from functools import lru_cache

fib2 = lru_cache(maxsize=None)(fib)

# this is much better, as the recursive calls will use the memoized version
@lru_cache(maxsize=None)
def fib3(n):
    if n < 2:
        return n
    return fib3(n-1) + fib3(n-2)

# iterative solution using a generator

def fibs():
    prev, curr = 0, 1
    yield prev
    yield curr
    while True:
        prev, curr = curr, prev + curr
        yield curr
    
def fibs_n(n):
    for i, v in enumerate(fibs()):
        if i >= n:
            break
        yield v