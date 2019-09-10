from enum import Enum, auto
from collections import namedtuple

class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

class Token(AutoName):
    LPAREN = auto()
    RPAREN = auto()
    PLUS = auto()
    TIMES = auto()
    NUMBER = auto()
    LET = auto()
    ID = auto()
    ASSIGN = auto()
    IN = auto()
    EOF = auto()

# I always wanted to do this!!
all_tokens = list(Token)

TokenInfo = namedtuple('TokenInfo', ['tag', 'value'])

def token(tag):
    return TokenInfo(tag=tag, value=None)

def tokenize(s):
    """Tokenize the given string s into a generator of tokens."""

    simple_tokens = {
        "(": Token.LPAREN,
        ")": Token.RPAREN,
        "+": Token.PLUS,
        "*": Token.TIMES,
    }

    unchar = None
    # note: we add the sentinel at the end to make sure
    # the number will be consumed in full
    iterator = iter(s + " ")
    while True:
        try:
            if unchar is not None:
                char = unchar
                unchar = None
            else:
                char = next(iterator)
            
            if char.isdigit():
                number = 0
                while char.isdigit():
                    number *= 10
                    number += int(char)
                    char = next(iterator)
                assert(char is not None)
                unchar = char
                yield TokenInfo(tag = Token.NUMBER, value = number)
                
            elif char in simple_tokens:
                yield token(simple_tokens[char])
            elif char == " " or char == "\n":
                continue
            # elif char == ":"

            elif char.isalnum():
                pass
            else:
                raise Exception(f"found unknown character while tokenizing: [{char}]")
        except StopIteration:
            break    
    yield token(Token.EOF)

def simplify(tokens):
    for (tag, value) in tokens:
        name = tag.name
        if value:
            yield name, value
        else:
            yield name

if __name__ == "__main__":
    example = "(1 + 11 * 22)"
    print(example)
    print(list(simplify(tokenize(example))))

    example2 = "let x := 1 in x + x"
    print(example2)
    print(list(simplify(tokenize(example2))))
