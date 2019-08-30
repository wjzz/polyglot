"""
Generation of various statistics for TTT.

We use various generators and the minimax algorithm.
"""

import sys
from collections import Counter, defaultdict

from common import TTT 
import generator as gen
from minimax import Minimax

#------------------------------------------------------------------------
# CALCULATING THE NUMBER OF UNIQUE POSITIONS
#------------------------------------------------------------------------

def total_unique_positions(gen):
    u_pos = set()
    for board in gen:
        u_pos.add(str(board))
    return len(u_pos)

def calculate_unique_terminal_positions():
    board = TTT()
    terminal = total_unique_positions(gen.all_terminal_positions(board))
    print(f"Found {terminal} unique terminal positions in the game tree.")    

def calculate_unique_positions():
    board = TTT()
    all = total_unique_positions(gen.all_positions(board))
    print(f"Found {all} unique positions in the game tree.")

def count(gen):
    return sum(1 for x in gen)

def calculate_unique_positions_memo():
    board = TTT()
    all = count(gen.all_positions_unique(board))
    print(f"Found {all} unique positions in the game tree.")

#------------------------------------------------------------------------
# TRAVERSING THE WHOLE GAME TREE WITH MEMOIZATION
#------------------------------------------------------------------------

# terrible algorithm, we leave it only for reference
def results_stats():
    counter = defaultdict(int)
    
    for index, board in enumerate(gen.all_positions_unique(TTT())):
        hash = str(board)
        evaluation = Minimax.minimax(9, board)
        counter[evaluation] += 1
        print(f"{index+1}: {hash} ==> {evaluation}")

    print(counter)

# nice, quick and short!
def results_stats_memo():
    memo = dict()
    
    # evaluate the whole game tree
    Minimax.minimax_memo(9, TTT(), memo)

    counter = Counter(memo.values())
    print(counter)

#------------------------------------------------------------------------
# THE MAIN FUNCTION
#------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        if flag == "terminal":
            calculate_unique_terminal_positions()
        elif flag == "unique":
            calculate_unique_positions()
        elif flag == "unique_memo":
            calculate_unique_positions_memo()
        elif flag == "results":
            results_stats()
        elif flag == "results_memo":
            results_stats_memo()
    else:
        print("Please provide an argument: terminal, unique, unique_memo, results, results_memo")
        sys.exit(1)
