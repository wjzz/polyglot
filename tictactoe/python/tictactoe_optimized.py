"""
The same as common.py but with a complicated, but somewhat optimized
winner function.

TODO: extend the TTT class using inheritance and remove duplication
"""

from common import TTT as Base, Piece

class TTT(Base):
    @property
    def winner(self):
        print("hhh")
        if (self.board[0] != Piece.E and (
            (self.board[0] == self.board[1] == self.board[2]) or
            (self.board[0] == self.board[3] == self.board[6]) or
            (self.board[0] == self.board[4] == self.board[8]))):
            return self.board[0]

        if (self.board[1] != Piece.E and 
           self.board[1] == self.board[4] == self.board[7]):
           return self.board[1]

        if (self.board[2] != Piece.E and (
            (self.board[2] == self.board[5] == self.board[8]) or
            (self.board[2] == self.board[4] == self.board[6]))):
            return self.board[2]

        if (self.board[3] != Piece.E and 
           self.board[3] == self.board[4] == self.board[5]):
           return self.board[3]

        if (self.board[6] != Piece.E and 
           self.board[6] == self.board[7] == self.board[8]):
           return self.board[6]

        return None
