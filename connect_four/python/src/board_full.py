from enum import Enum
from random import choice

class Piece(Enum):
    X = "X"
    O = "O"
    E = "."

    @property
    def opposite(self):
        if self == Piece.X:
            return Piece.O
        elif self == Piece.O:
            return Piece.X
        else:
            return Piece.E

    @property
    def not_empty(self):
        return self != Piece.E

    def __str__(self):
        return self.value

class Config:
    ROWS = 6
    COLS = 7

class Board:
    @classmethod
    def constr(cls, cols, current, last, prev_hash=None):
        """
        Initializes a board from the given state.
        """
        # construct an empty board
        b = cls()

        # find the first empty space for each col
        lens = []
        for col in cols:
            row = 0
            while row < Config.ROWS and col[row].not_empty:
                row += 1
            lens.append(row)

        b._current = current
        b._cols = cols
        b._last = last
        b._lasts = [None, last]
        b._lens = lens
        
        # FIXME: implement this
        b._myhash = -1

        b._invariant()

        return b

    def __init__(self):
        """
        Initializes an empty board.
        """
        empty_cols = [ [Piece.E] * Config.ROWS for _ in range(Config.COLS) ]
        empty_lens = [0] * Config.COLS

        self._current = Piece.X
        self._cols = empty_cols
        self._last = None
        self._lasts = [None]
        self._lens = empty_lens
        
        # TODO: add a "moves_made" property

        # FIXME: implement hashing
        self._myhash = -1 

        self._invariant()

    def _invariant(self):
        """
        Checks if various invariants hold for the current instance.
        """

        # check the sizes of the cols:
        assert(len(self._cols) == Config.COLS)
        for col in self._cols:
            assert(len(col) == Config.ROWS)

        # check if current player is correct
        moves_made = sum( sum(1 for piece in col if piece.not_empty) 
                          for col in self._cols)

        if moves_made % 2 == 0:
            assert(self._current == Piece.X)
        else:
            assert(self._current == Piece.O)

        # check the last property

        # self._last is None    <=>        moves_made == 0
        if moves_made == 0:
            assert(self._last is None)
        else:
            assert(self._last is not None)

        # the lens properties
        # self._lens[cc] is the index the of the first empty
        # field (or equivalently: it's the number of pieces
        # in the given column)
        for cc, col in enumerate(self._cols):
            stored_len = self._lens[cc]
            assert(stored_len <= len(col))
            if stored_len < len(col):
                assert(col[stored_len] == Piece.E)
                for i in range(stored_len):
                    assert(col[i].not_empty)
        
    def __eq__(self, other):
        return str(self) == str(other)
        # return ((self._current, self._last, self._cols) 
        #         == (other._current, other._last, other._cols))

    def __str__(self):
        output = ""
        for row in reversed(range(Config.ROWS)):
            output += f"{row + 1} "
            for col in self._cols:
                output += str(col[row])
            output += "\n"
        output += f"last = {self._last}\n"
        return output

    # NOTE: this is more like a full encoding that merely a hash
    @property
    def myhash(self):
        return self._myhash
        
    @property
    def str_hash(self):
        output = ""
        for row in reversed(range(Config.ROWS)):
            for col in self._cols:
                output += str(col[row])
        return output

    @classmethod
    def from_str(cls, s):
        lines = s.splitlines()
        assert(len(lines) == Config.ROWS + 1)

        non_empty = 0
        cols = [ [Piece.E] * Config.ROWS for _ in range(Config.COLS) ]
        for row_idx, row in enumerate(reversed(lines[:-1])):
            row = row[2:]
            assert(len(row) == Config.COLS)
            for col, field in enumerate(row):
                if field != ".":
                    non_empty +=1
                cols[col][row_idx] = Piece(field)
        
        last_line_parts = lines[-1].split(" = ")
        assert(len(last_line_parts) == 2)
        last_str = last_line_parts[1]
        last = None if last_str == "None" else int(last_str)

        current = Piece.X if non_empty % 2 == 0 else Piece.O

        return Board.constr(cols, current, last)

    @property
    def legal_moves(self):
        return [ i for i, col in enumerate(self._cols) 
                 if col[-1] == Piece.E ]

    def apply_move(self, move):
        # assert (self._cols[move][-1] == Piece.E)
        cols = [ col.copy() for col in self._cols ]
        
        # find empty row
        i = 0
        while cols[move][i] != Piece.E:
            i += 1
        cols[move][i] = self._current

        return Board.constr(cols, 
            current = self._current.opposite, 
            last = move, 
            prev_hash = self.myhash)

    # TODO: write unittests for make/unmake moves

    def make_move(self, move):
        self._lasts.append(move)
        self._last = move
        player = self._current

        self._cols[move][self._lens[move]] = player
        self._lens[move] += 1
        self._current = player.opposite

    def unmake_move(self, move):
        last = self._last
        self._lens[last] -= 1

        player = self._current
        self._current = player.opposite
        self._cols[last][self._lens[last]] = Piece.E
        self._lasts.pop()
        self._last = self._lasts[-1]
     
    @property
    def is_win(self):
        # TODO: optimization
        # there must be at least 7 moves for a win
        if self._last is None:
            return False
        # TODO: optimization - we don't have to go up
        return (self._check_line(0, 1)
             or self._check_line(1, 0)
             or self._check_line(1, 1)
             or self._check_line(1, -1))

    def _check_line(self, dx, dy):
        a = self._check_straight_line(dx, dy)
        b = self._check_straight_line(-dx, -dy)
        return a + b + 1 >= 4

    def _check_straight_line(self, dx, dy):
        col = self._last
        assert(col != None)
        cols = self._cols
        player = self._current.opposite
        assert (player != Piece.E)

        # TODO: this can be easily optimized
        # find the last move

        # FIXME: this doesn't work
        # row = self._lens[col] - 1

        # iefficient but correct way of calculating the row
        # of the last move played
        row = 0
        assert(cols[col][row] != Piece.E)
        while row + 1 < Config.ROWS and cols[col][row+1] != Piece.E:
           row += 1
        assert(cols[col][row] == player)

        in_line = 0
        cc, cr = col + dx, row + dy
        while 0 <= cc < Config.COLS and 0 <= cr < Config.ROWS:
            ccol = cols[cc]
            if cr >= Config.ROWS or ccol[cr] != player:
                break
            in_line += 1
            cc, cr = cc + dx, cr + dy
        return in_line
    
    @property
    def is_draw(self):
        # TODO: this can be easily optimized
        # by counting moves made so far
        return [] == self.legal_moves

    @property
    def is_finished(self):
        return self.is_win or self.is_draw

    @property
    def evaluate(self):
        """
        Evaluates the current position.
        
        Returns:
            1 - game has just been won
            0 - the game is a draw
            None - the game is not yet finished
        """
        if self.is_win:
            return 1
        if self.is_draw:
            return 0
        return None

    def succesors(self, depth):
        """
        A generator containing all successor nodes 
        coming from the given position.

        For clarity, it uses the immutable 
        version of making the move.
        """
        def iter(board, depth):
            yield board
            if depth > 0 and not board.is_finished:
                for move in board.legal_moves:
                    yield from iter(board.apply_move(move), depth-1)
        
        yield from iter(self, depth)

    def succesors_mut(self, depth):
        """
        A generator containing all successor node hashes
        coming from the given position.

        We don't return the boards, because the pointers
        will be invalid.

        For performance, it uses the mutable version of
        making and unmaking the move.
        """
        def iter(board, depth):
            yield board.str_hash
            if depth > 0 and not board.is_finished:
                for move in board.legal_moves:
                    board.make_move(move)
                    yield from iter(board, depth-1)
                    board.unmake_move(move)
        
        yield from iter(self, depth)

    def visit_all_mut(self, depth, visitor):
        """
        Visits all nodes starting from the current one until the given depth
        and performs some imperative action.
        """
        def iter(board, depth):
            visitor(board)
            if depth > 0 and not board.is_finished:
                for move in board.legal_moves:
                    board.make_move(move)
                    iter(board, depth-1)
                    board.unmake_move(move)
        
        iter(self, depth)
