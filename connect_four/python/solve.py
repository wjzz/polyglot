from board import Board, Piece, Config
from time import time
import sys

class Stats:
    finished = 0
    total = 0
    terminal = 0

    @classmethod
    def reset(cls):
        cls.finished = 0
        cls.total = 0
        cls.terminal = 0

def search_all(board, depth):
    """
    Search the whole game tree starting from BOARD and
    going at move DEPTH moves from BOARD,
    ie. we stop recursion at depth == 0
    """
    Stats.total += 1
    if depth == 0:
        Stats.terminal += 1
    if board.is_finished:
        if depth == 0:
            Stats.finished += 1
    elif depth >= 1:
        for move in board.legal_moves:
            search_all(board.apply_move(move), depth-1) 

def search_all_memo(board, depth, memo):
    """
    Search the whole game tree starting from BOARD and
    going at move DEPTH moves from BOARD,
    ie. we stop recursion at depth == 0

    This version uses memoization to ensure that we don't expand the same node twice.
    Note that we don't have to store the depth in the memo, since
    """
    # h = board.str_hash
    h = board.myhash
    if h not in memo:
        Stats.total += 1
        if depth == 0:
            Stats.terminal += 1
        if board.is_finished:
            if depth == 0:
                Stats.finished += 1
        elif depth >= 1:
            for move in board.legal_moves:
                search_all_memo(board.apply_move(move), depth-1, memo)
        memo.add(h)

def search_all_memo_top(board, depth):
    memo = set()
    search_all_memo(board, depth, memo)
    # memo_size = sys.getsizeof(memo)
    # val, suf = humanize_bytes(memo_size)
    # print(f"\nmemo size = {int(val)}{suf}")
    return len(memo)


def humanize_bytes(seconds):
    value = seconds
    suffixes = ["b", "kb", "mb", "gb", "tb"]
    divisors = [1024] * len(suffixes)
    for suffix, divisor in zip(suffixes, divisors):
        if value < divisor:
            return (value, suffix)
        value /= divisor

def humanize(seconds):
    value = seconds
    suffixes = ["s", "m", "h", "d", "y"]
    divisors = [60, 60, 24, 365, 10000]
    for suffix, divisor in zip(suffixes, divisors):
        if value < divisor:
            return (value, suffix)
        value /= divisor

def print_time_estimate(depth, times):
    if times:
        if len(times) > 1:
            den = max(0.1, times[-2])
            estimate = (times[-1] ** 2) / den
        else:
            estimate = times[-1] * Config.COLS
        
        est_time, suffix = humanize(estimate)
        print(f"Current depth: {depth} "
            f"estimated time: {est_time:.2f}{suffix}",
            flush=True, 
            end="")

if __name__ == "__main__":
    Config.COLS = 7
    Config.ROWS = 6

    print(f"Current size [COLS x ROWS]: {Config.COLS} x {Config.ROWS}")
    prev_times = []
    for depth in range(17):
        Stats.reset()
        print_time_estimate(depth, prev_times)
        start = time()
        memo_size = 0
        # search_all(Board(), depth)
        memo_size = search_all_memo_top(Board(), depth)
        end = time()
        time_diff = end - start
        prev_times.append(time_diff)
        elapsed, suffix = humanize(time_diff)
        
        if Stats.terminal > 0:
            percentage = 100 * Stats.finished // Stats.terminal
        else:
            percentage = 100

        print(f"\rDepth {depth:2}: {Stats.total:13,} "
              f"states in {elapsed:2.2f}{suffix} "
              f"[{percentage}%] {Stats.finished:,} / {Stats.terminal:,} "
              f"[memo size: {memo_size:,}]"
              )
