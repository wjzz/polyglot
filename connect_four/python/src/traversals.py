# from board import Config, Board

def traverse_all_immutable(board, depth):
    """
    A generator that traverses the whole game tree
    without any optimizations.
    """
    yield board
    if depth >= 1 and not board.is_finished:
        for move in board.legal_moves:
            yield from traverse_all_immutable(board.apply_move(move), depth-1)

def traverse_unique_immutable(board, depth):
    memo = set()
    def iter(board, depth):
        h = board.myhash
        if h not in memo:
            yield board
            memo.add(h)
            if depth >= 1 and not board.is_finished:
                for move in board.legal_moves:
                    yield from iter(board.apply_move(move), depth-1)
    yield from iter(board, depth)


def count_all_mutable_top(board, depth):
    """
    Counts the number of nodes in the game tree.
    """
    total = 0
    def iter(depth):
        nonlocal total
        total += 1
        if depth >= 1 and not board.is_finished:
            for move in board.legal_moves:
                board.make_move(move)
                iter(depth-1) 
                board.unmake_move(move)
    iter(depth)
    return total


def count_all_top(board, depth):
    """
    Counts the number of nodes in the game tree.
    """
    total = 0
    def iter(board, depth):
        nonlocal total
        total += 1
        if depth >= 1 and not board.is_finished:
            for move in board.legal_moves:
                iter(board.apply_move(move), depth-1) 
    iter(board, depth)
    return total

def count_all_unique_top(board, depth):
    """
    Counts the number of unique nodes in the game tree.
    """
    total = 0
    memo = set()
    def iter(board, depth):
        nonlocal total
        h = board.myhash
        if h not in memo:
            total += 1
            memo.add(h)
            if depth >= 1 and not board.is_finished:
                for move in board.legal_moves:
                    iter(board.apply_move(move), depth-1) 
    iter(board, depth)
    return total
    