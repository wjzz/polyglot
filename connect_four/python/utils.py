"""
Random helper functions
"""

def humanize_bytes(seconds):
    value = seconds
    suffixes = ["b", "kb", "mb", "gb", "tb"]
    divisors = [1024] * len(suffixes)
    for suffix, divisor in zip(suffixes, divisors):
        if value < divisor:
            return (value, suffix)
        value /= divisor

def humanize_time(seconds):
    value = seconds
    suffixes = ["s", "m", "h", "d", "y"]
    divisors = [60, 60, 24, 365, 10000]
    for suffix, divisor in zip(suffixes, divisors):
        if value < divisor:
            return (value, suffix)
        value /= divisor
