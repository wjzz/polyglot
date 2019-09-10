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

    reading_number = False
    number = 0
    # note: we add the sentinel at the end to make sure
    # the number will be consumed in full
    for char in s + " ":
        if not char.isdigit() and reading_number:
            yield TokenInfo(tag = Token.NUMBER, value = number)
            reading_number = False
            number = 0
        if char.isdigit():
            reading_number = True
            number *= 10
            number += int(char)
        elif char in simple_tokens:
            yield token(simple_tokens[char])
        elif char == " " or char == "\n":
            continue
        
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
