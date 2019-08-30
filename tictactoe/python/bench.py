"""
Benchmarks for the minimax algorithm. 

We use two implementantions:
a) Minimax (immutable flag)
b) MinimaxMutable (mutable flag)

a) uses immutable operations on the board, while
b) uses make and unmake move and it mutates the argument board.
"""

import sys
from common import TTT
from minimax import Counter, Minimax, MinimaxMutable

if __name__ == "__main__":
    board = TTT()
    Counter.reset()
    depth = 8

    if len(sys.argv) > 1 and sys.argv[1] == "immutable":
        best_move = Minimax.best_move(board, depth)
    elif len(sys.argv) > 1 and sys.argv[1] == "mutable":
        best_move = MinimaxMutable.best_move(board, depth)
    else:
        print("no arguments given!", file=sys.stderr)
        sys.exit(1)

    #print("Best move: ", best_move)
    print(f"total terminal states: {Counter.total}")
