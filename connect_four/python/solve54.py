from board import Board, Piece, Config
from utils import humanize_time, humanize_bytes
from time import time
import sys

class Stats:
    finished = 0
    total = 0
    terminal = 0
    start = 0
    end = 0

    @classmethod
    def reset(cls):
        cls.finished = 0
        cls.total = 0
        cls.terminal = 0
        cls.start = 0
        cls.end = 0

#-------------------------------------------------------
#           SOLVING THE WHOLE GAME TREE
#-------------------------------------------------------

TOTAL44 = 131060741
TOTAL55 = 289156574

def solve_game(board, depth):
    """
    Computes the theoretical result of the current position.
    
    The return value is:
         1 when the current player wins
         0 when the game ends in a draw with optimal play
        -1 when the other player wins
    """

    Stats.total += 1
    # if Stats.total % 1000000 == 0:
    #     Stats.end = time()
    #     time_diff = Stats.end - Stats.start
    #     amount, suffix = humanize_time(time_diff)
    #     percentage = (100 * Stats.total) / TOTAL
    #     print(f"visited {Stats.total // 1000000}M nodes [{percentage:.2f}%]"
    #           f" in {amount:.2f}{suffix}"
    #     )

    # this will never be -1, because we don't go that far
    evaluation = board.evaluate

    if evaluation is not None:
        if evaluation == 1:
            # this means we have just lost
            return -1
        else:
            return 0
    if depth == 0:
        raise RecursionError
        
    # we use the negamax schema
    # our best result is the worst result of the opponent
    return -1 * min([solve_game(board.apply_move(move), depth-1) 
                     for move in board.legal_moves])

def solve_game_top(board, depth = Config.COLS * Config.ROWS):
    """
    Traverses the whole game tree and calculates the optimal outcome.
    """
    print(f"Starting search at depth = {depth}")
    Stats.start = time()
    return solve_game(board, depth)

#-------------------------------------------------------
#      SOLVING THE WHOLE GAME TREE WITH MEMOIZATION
#-------------------------------------------------------

def solve_game_memo(board, depth, memo, moves_made):
    """
    Computes the theoretical result of the current position.
    
    The return value is:
         1 when the current player wins
         0 when the game ends in a draw with optimal play
        -1 when the other player wins
    """

    h = board.myhash

    CUT_OFF = 20

    if h not in memo:
        Stats.total += 1
        if Stats.total % 2500000 == 0:
            Stats.end = time()
            time_diff = Stats.end - Stats.start
            amount, suffix = humanize_time(time_diff)
            percentage = (100 * Stats.total) / TOTAL55
            print(f"visited {Stats.total // 1000}k nodes [{percentage:.2f}%]"
                f" in {amount:.2f}{suffix}"
            )

        # this will never be -1, because we don't go that far
        evaluation = board.evaluate

        if evaluation is not None:
            if evaluation == 1:
                # this means we have just lost
                result = -1
            else:
                result = 0
        elif depth == 0:
            raise RecursionError
        else:        
            # we use the negamax schema
            # our best result is the worst result of the opponent
            result =  -1 * min([solve_game_memo(board.apply_move(move), depth-1, memo, moves_made+1) 
                            for move in board.legal_moves])
        if moves_made < CUT_OFF:
            memo[h] = result
        else:
            return result
    return memo[h]

def solve_game_memo_top(board, depth = Config.COLS * Config.ROWS):
    """
    Traverses the whole game tree and calculates the optimal outcome.
    """
    print(f"Starting search at depth = {depth}")
    Stats.start = time()
    memo = {}
    return solve_game_memo(board, depth, memo, moves_made=0)

#-------------------------------------------------------
#           SEARCHING THE WHOLE GAME TREE
#-------------------------------------------------------

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


#-------------------------------------------------------
#    SEARCHING THE WHOLE GAME TREE WITH MEMOIZATION
#-------------------------------------------------------

def search_all_memo(board, depth, memo, moves_made):
    """
    Search the whole game tree starting from BOARD and
    going at move DEPTH moves from BOARD,
    ie. we stop recursion at depth == 0

    This version uses memoization to ensure that we don't expand the same node twice.
    Note that we don't have to store the depth in the memo, since
    """
    # h = board.str_hash
    CUT_OFF = 21
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
                search_all_memo(board.apply_move(move), depth-1, memo, moves_made + 1)
        if moves_made < CUT_OFF:
            memo.add(h)

def search_all_memo_top(board, depth):
    memo = set()
    search_all_memo(board, depth, memo, 0)
    # memo_size = sys.getsizeof(memo)
    # val, suf = humanize_bytes(memo_size)
    # print(f"\nmemo size = {int(val)}{suf}")
    return len(memo)

#-------------------------------------------------------
# DRIVERS FOR RUNNING THE SEARCHES AND COLLECTING STATS
#-------------------------------------------------------

def print_time_estimate(depth, times):
    if times:
        if len(times) > 1:
            den = max(0.1, times[-2])
            estimate = (times[-1] ** 2) / den
        else:
            estimate = times[-1] * Config.COLS
        
        est_time, suffix = humanize_time(estimate)
        print(f"Current depth: {depth} "
            f"estimated time: {est_time:.2f}{suffix}",
            flush=True, 
            end="")

def search_all_main(start = 0):
    prev_times = []
    MAX_DEPTH = Config.COLS * Config.ROWS
    print(f"Max depth = {MAX_DEPTH}")
    for depth in range(start, MAX_DEPTH + 1):
        Stats.reset()
        print_time_estimate(depth, prev_times)
        start = time()
        memo_size = 0
        # search_all(Board(), depth)
        memo_size = search_all_memo_top(Board(), depth)
        end = time()
        time_diff = end - start
        prev_times.append(time_diff)
        elapsed, suffix = humanize_time(time_diff)
        
        if Stats.terminal > 0:
            percentage = 100 * Stats.finished // Stats.terminal
        else:
            percentage = 100

        print(f"\rDepth {depth:2}: {Stats.total:13,} "
            f"states in {elapsed:2.2f}{suffix} "
            f"[{percentage}%] {Stats.finished:,} / {Stats.terminal:,} "
            f"[memo size: {memo_size:,}]"
            )

def solve_game_main():
    try:
        result = solve_game_memo_top(Board(), Config.COLS * Config.ROWS)
    except RecursionError:
        result = "Not deep enough"
    print(f"Game solved. Result = {result}")
    print(f"[1 = first player wins, -1 = second player wins, 0 = draw]")
    print(f"Total visited nodes = {Stats.total:,}")

#-------------------------------------------------------
#                  THE STARTING POINT
#-------------------------------------------------------

if __name__ == "__main__":
    Config.COLS = 5
    Config.ROWS = 4

    print(f"Current size [COLS x ROWS]: {Config.COLS} x {Config.ROWS}")
    #search_all_main(19)
    solve_game_main()
    