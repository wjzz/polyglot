from lexer import tokenize, Token, TokenInfo
import expr as E

# TOP ::= <EXPR> EOF
# EXPR ::= <FACTOR> | <FACTOR> + <EXPR>
# FACTOR ::= <ATOM> | <ATOM> * <FACTOR>
# ATOM = NUM | ( <EXPR> )

class Parser:
    def __init__(self, tokens):
        self._tokens = tokens

    @property
    def get_token(self):
        return next(self._tokens)

    @property
    def peek(self):
        self._tokens = self.peekable(self._tokens)
        return next(self._tokens)

    def peekable(self, gen):
        val = next(gen)
        yield val
        yield val
        yield from gen

    def expect(self, expected_tag):
        token = self.get_token
        assert(token.tag == expected_tag)

    def parse_top(self):
        e = self.parse_expr()
        self.expect(Token.EOF)
        return e

    def parse_expr(self):
        factor = self.parse_factor()
        token = self.peek
        if token.tag != Token.PLUS:
            return factor
        else:
            self.expect(Token.PLUS)
            expr = self.parse_expr()
            return E.BinaryOp(factor, E.Op.Plus, expr)


    def parse_factor(self):
        atom = self.parse_atom()
        token = self.peek
        if token.tag != Token.TIMES:
            return atom
        else:
            self.expect(Token.TIMES)
            factor = self.parse_factor()
            return E.BinaryOp(atom, E.Op.Mult, factor)

    def parse_atom(self):
        token = self.get_token
        if token.tag == Token.LPAREN:
            e = self.parse_expr()
            self.expect(Token.RPAREN)
            return e
        elif token.tag == Token.NUMBER:
            return E.NumberLit(token.value)

def parse(s):
    """Takes an input string and output an expr AST"""
    tokens = tokenize(s)
    print(list(tokenize(s)))
    return Parser(tokens).parse_top()
