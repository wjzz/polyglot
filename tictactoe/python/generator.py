"""
Generator functions for enumerating the whole game tree.

They are general and should work with any board game.
"""

def all_positions(board):
    yield board

    if not board.is_finished:
        for move in board.legal_moves:
            yield from all_positions(board.apply(move))

def all_positions_unique(board, memo = set()):
    hash = str(board)

    if hash not in memo:
        yield board

        memo.add(hash)
        if not board.is_finished:
            for move in board.legal_moves:
                yield from all_positions_unique(board.apply(move), memo)
     

def all_terminal_positions(board):
    if board.is_finished:
        yield board
    else:
        for move in board.legal_moves:
            yield from all_terminal_positions(board.apply(move))
