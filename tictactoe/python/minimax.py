"""
Generic implementations of the minimax algorithm.
"""

class Counter:
    @staticmethod
    def reset():
        Counter.total = 0

Counter.total = 0

class Minimax:
    @staticmethod
    def minimax_memo(depth, board, memo = dict()):
        hash = str(board)
        
        if hash not in memo:
            if depth <= 0 or board.is_finished:
                Counter.total += 1
                memo[hash] = board.evaluate        
            else:
                # we use the negamax trick, so that we don't have to
                # use max and min depending on the depth
                memo[hash] = max(-1 * Minimax.minimax_memo(depth-1, board.apply(move), memo)
                    for move in board.legal_moves)

        return memo[hash]

    @staticmethod
    def minimax(depth, board):
        if depth <= 0 or board.is_finished:
            Counter.total += 1
            return board.evaluate
        
        # we use the negamax trick, so that we don't have to
        # use max and min depending on the depth
        return max(-1 * Minimax.minimax(depth-1, board.apply(move))
            for move in board.legal_moves)

    @staticmethod
    def best_move(board, max_depth):
        best_move = None
        best_eval = -100

        for move in board.legal_moves:
            value = Minimax.minimax(max_depth-1, board.apply(move))
            #print(f"move {move} has value {value}")

            if value > best_eval:
                best_eval = value
                best_move = move
        return best_move

class MinimaxMutable:
    @staticmethod
    def minimax(depth, board):
        if depth <= 0 or board.is_finished:
            # we don't change this to simplify
            Counter.total += 1
            return board.evaluate
        
        # we use the negamax trick, so that we don't have to
        # use max and min depending on the depth
        result = -100

        for move in board.legal_moves:
            board.make_move(move)
            value = -1 * MinimaxMutable.minimax(depth-1, board)
            result = max(value, result)
            board.unmake_move(move)
        return result

    @staticmethod
    def best_move(board, max_depth):
        best_move = None
        best_eval = -100

        for move in board.legal_moves:
            board.make_move(move)
            value = MinimaxMutable.minimax(max_depth-1, board)
            #print(f"move {move} has value {value}")

            if value > best_eval:
                best_eval = value
                best_move = move
            board.unmake_move(move)
        return best_move
