"""
Comparison of two versions of TTT
"""

import common
import tictactoe_optimized as optimized
import generator as gen
from minimax import Minimax

def get_memo(initial_board):
    memo = dict()
    Minimax.minimax_memo(9, initial_board, memo)
    return memo

def compare_memos():
    memo1 = get_memo(common.TTT())
    memo2 = get_memo(optimized.TTT())

    print(f"lens are equal = {len(memo1) == len(memo2)}")
    print(f"len = {len(memo1)}")

    for k in memo1.keys():
        if k not in memo2 or memo1[k] != memo2[k]:
            print(f"Different values for {k}")
            print(f"memo1 = {memo1[k]}, memo2 = {memo2[k]}")
            return
    
    print("memos are equal!")


if __name__ == "__main__":
    compare_memos()