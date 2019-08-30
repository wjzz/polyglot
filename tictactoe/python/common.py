"""
Basic implementation of the Tic Tac Toe game. 

Contains definitions of the Piece type and the TTT type.
"""

from enum import Enum

class Piece(Enum):
    X = 1
    O = 2
    E = 3
    
    def __str__(self):
        if self == Piece.X:
            return "X"
        elif self == Piece.O:
            return "O"
        else:
            return "."

    @property
    def opposite(self):
        if self == Piece.X:
            return Piece.O
        elif self == Piece.O:
            return Piece.X
        else:
            return Piece.E

class TTT:
    def __init__(self, board = [Piece.E] * 9, player = Piece.X):
        self.board = board
        self.current = player

    def __str__(self):
        return "".join(str(piece) for piece in self.board)

    @property
    def current_player(self):
        return self.current

    @property
    def evaluate(self):
        winner = self.winner
        if winner == self.current_player:
            return 1
        elif winner == self.current_player.opposite:
            return -1
        else:
            return 0

    @property
    def is_finished(self):
        return self.winner != None or self.is_draw

    @property
    def is_draw(self):
        return not self.legal_moves

    # mutable version
    def make_move(self, move):
        self.board[move] = self.current
        self.current = self.current.opposite

    def unmake_move(self, move):
        self.board[move] = Piece.E
        self.current = self.current.opposite

    # immutable version
    def apply(self, move):
        board = self.board.copy()
        board[move] = self.current
        player = self.current.opposite
        return TTT(board, player)

    @property
    def legal_moves(self):
        return [i for i in range(9) if self.board[i] == Piece.E]

    def is_line(self, a, b, c):
        return (self.board[a] != Piece.E
            and self.board[a] == self.board[b]
            and self.board[b] == self.board[c])

    @property
    def winner(self):
        lines = [[0, 1, 2], 
                 [3, 4, 5],
                 [6, 7, 8],
                 [0, 3, 6],
                 [1, 4, 7],
                 [2, 5, 8],
                 [0, 4, 8],
                 [2, 4, 6],
                ]
        for [a,b,c] in lines:
            result = self.is_line(a,b,c)
            if result:
                return self.board[a]
        return None

    @property
    def nodes(self):
        yield self

        if not self.is_finished:
            for move in self.legal_moves:
                yield from self.apply(move).nodes
    