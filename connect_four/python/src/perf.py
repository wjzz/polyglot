"""
Simple comparison of the performance of various board
representations.
"""

from time import time

import board
import board_full

def visit_all_nodes_immut(board, depth):
    total = 0
    def iter(board, depth):
        nonlocal total
        total += 1
        if depth > 0 and not board.is_finished:
            for move in board.legal_moves:
                iter(board.apply_move(move), depth-1)
    iter(board, depth)
    return total

def visit_all_nodes_mut(board, depth):
    total = 0
    def iter(board, depth):
        nonlocal total
        total += 1
        if depth > 0 and not board.is_finished:
            for move in board.legal_moves:
                board.make_move(move)
                iter(board, depth-1)
                board.unmake_move(move)
    iter(board, depth)
    return total

def benchmark(board, depth, mut=False):
    start = time()
    if mut:
        result = visit_all_nodes_mut(board, depth)
    else:
        result = visit_all_nodes_immut(board, depth)
    end = time()

    elapsed = end - start
    return (result, elapsed)

if __name__ == "__main__":
    for depth in range(10):
        print(f"Depth = {depth}:")
        print(f"  [board]            = {benchmark(board.Board(), depth)}")
        print(f"  [board_full_mut]   = {benchmark(board_full.Board(), depth, mut=True)}")
        #print(f"  [board_full_immut] = {benchmark(board_full.Board(), depth)}")
