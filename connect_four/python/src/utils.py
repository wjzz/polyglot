"""
Random helper functions
"""

from time import time

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

class Timer():
    def __enter__(self):
        self.start = time()

    def __exit__(self, type, value, traceback):
        self.end = time()

    def __str__(self, verbose=False):
        if verbose:
            prompt = "Elapsed time: "
        else:
            prompt = ""

        elapsed, suffix = humanize_time(self.end - self.start)
        return f"{prompt}{elapsed:.1f}{suffix}"
    
    @property
    def seconds(self):
        if not self.start or not self.end:
            raise ValueError("timer not finished yet")
        return self.end - self.start

if __name__ == "__main__":
    # takes around 4 seconds
    with Timer():
        sum(1 for _ in range(100 * 1000 * 1000))