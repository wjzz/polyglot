"""
Using decorators to memoize functions
"""

from functools import lru_cache

def memo(fun):
    cache = {}
    def wrapper(*args, **kwargs):
        argument = args # (args, kwargs)
        # TODO: kwargs is not hashable
        # we can serialize it 
        if argument not in cache:
            value = fun(*args, **kwargs)
            cache[argument] = value
        return cache[argument]
    
    # it's good practice to do this
    wrapper.__name__ = fun.__name__
    return wrapper

#-----------------------------------------

def fib_slow(n):
    if n < 2:
        return n
    return fib_slow(n-1) + fib_slow(n-2)

@memo
def fib_quick(n):
    if n < 2:
        return n
    return fib_quick(n-1) + fib_quick(n-2)

@lru_cache(maxsize=None)
def fib_cache(n):
    if n < 2:
        return n
    return fib_cache(n-1) + fib_cache(n-2)
