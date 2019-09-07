from enum import Enum
from random import choice

class Piece(Enum):
    X = "X"
    O = "O"

    @property
    def opposite(self):
        if self == Piece.X:
            return Piece.O
        elif self == Piece.O:
            return Piece.X
        else:
            raise TypeError

    def __str__(self):
        return self.value

class Config:
    ROWS = 6
    COLS = 7

class Board:
    def __init__(self, cols = None, current = Piece.X, last = None, prev_hash = None):
        if not cols:
            cols = [ [] for _ in range(Config.COLS) ]

        self._cols = cols
        self._current = current
        self._last = last

        if prev_hash != None:
            assert(current != None and last != None)
            bits_to_move = 2 * (Config.ROWS * (Config.COLS - last) - len(cols[last]))
            if current.opposite == Piece.X:
                last_piece = 0b01
            else:
                last_piece = 0b10
            mask = last_piece << bits_to_move

            new_hash = prev_hash | mask
            # if (h != new_hash):
            #     # print()
            #     print(f"\nnew mask = [{mask:52b}] bits_to_move = {bits_to_move} last = {last}")
            #     print(f"old hash = [{h:52b}]")
            #     print(f"new hash = [{new_hash:52b}]")
            self._myhash = new_hash
        else:
            h = 1
            for col in self._cols:
                for piece in col:
                    h <<= 2
                    if piece == Piece.X:
                        h |= 0b01
                    else:
                        h |= 0b10
                h <<= 2 * (Config.ROWS - len(col))
            self._myhash = h

    def __eq__(self, other):
        return ((self._current, self._last, self._cols) 
                == (other._current, other._last, other._cols))

    def __str__(self):
        output = ""
        for row in reversed(range(Config.ROWS)):
            output += f"{row + 1} "
            for col in self._cols:
                if row < len(col):
                    output += str(col[row])
                else:
                    output += "."
            output += "\n"
        output += f"last = {self._last}\n"
        return output

    # TODO: write unit tests for this
    # NOTE: this is more like a full encoding that merely a hash
    @property
    def myhash(self):
        return self._myhash

        # h = 1
        # for col in self._cols:
        #     for piece in col:
        #         h <<= 2
        #         if piece == Piece.X:
        #             h |= 0b01
        #         else:
        #             h |= 0b10
        #     h <<= 2 * (Config.ROWS - len(col))
        # return h
        
    @property
    def str_hash(self):
        output = ""
        for row in reversed(range(Config.ROWS)):
            for col in self._cols:
                if row < len(col):
                    output += str(col[row])
                else:
                    output += "."
        return output

    @classmethod
    def from_str(cls, s):
        lines = s.splitlines()
        assert(len(lines) == Config.ROWS + 1)

        non_empty = 0
        cols = [ [] for _ in range(Config.COLS) ]
        for row in reversed(lines[:-1]):
            row = row[2:]
            assert(len(row) == Config.COLS)
            for col, field in enumerate(row):
                if field != ".":
                    non_empty +=1
                    cols[col].append(Piece(field))
        
        last_line_parts = lines[-1].split(" = ")
        assert(len(last_line_parts) == 2)
        last_str = last_line_parts[1]
        last = None if last_str == "None" else int(last_str)

        current = Piece.X if non_empty % 2 == 0 else Piece.O

        return Board(cols, current, last)

    @property
    def legal_moves(self):
        return [ i for i, col in enumerate(self._cols) 
                 if len(col) < Config.ROWS ]

    def apply_move(self, move):
        assert (len(self._cols[move]) < Config.ROWS)
        cols = [ col.copy() for col in self._cols ]
        cols[move].append(self._current)
        return Board(cols, self._current.opposite, last = move, prev_hash = self.myhash)
     
    @property
    def is_win(self):
        # TODO: optimization
        # there must be at least 7 moves for a win
        if self._last is None:
            return False
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
        cols = self._cols
        player = cols[col][-1]
        row = len(cols[col]) - 1

        in_line = 0
        cc, cr = col + dx, row + dy
        while 0 <= cc < Config.COLS and 0 <= cr < Config.ROWS:
            ccol = cols[cc]
            if cr >= len(ccol) or ccol[cr] != player:
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

def random_game_length():
    board = Board()
    moves = board.legal_moves
    i = 0
    while moves:
        move = choice(moves)
        board = board.apply_move(move)
        i += 1
        if board.is_win or board.is_draw:
            break
        else:
            moves = board.legal_moves
    return i

def random_game():
    board = Board()
    moves = board.legal_moves
    i = 0
    while moves:
        print(board)
        move = choice(moves)
        print(f"Turn {i}> Playing move: {move} out of {moves}")
        board = board.apply_move(move)
        i += 1
        if board.is_win:
            print("Game won!\n")
            break
        elif board.is_finished:
            print("Draw!\n")
            break
        else:
            moves = board.legal_moves
    print(board)

if __name__ == "__main__":
    GAMES = 5000
    total = 0
    for game in range(GAMES):
        moves_no = random_game_length()
        total += moves_no
        #print(f"Game #{game+1} finished after: {moves_no}")
    print(f"After {GAMES} games average = {total / GAMES}")