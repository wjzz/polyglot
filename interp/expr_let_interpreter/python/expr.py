from enum import Enum
from collections import namedtuple

class NumberLit(namedtuple('NumberLit', 'value')):
    def __str__(self):
        return str(self.value)
    
    def accept_visitor(self, visitor):
        return visitor.literal(self.value)

class Variable(namedtuple('Variable', 'name')):
    def __str__(self):
        return self.name

    def accept_visitor(self, visitor):
        return visitor.variable(self.name)

class Op(Enum):
    Plus = "+"
    Mult = "*"

class BinaryOp(namedtuple('BinaryOp', 'e1 op e2')):
    def __str__(self):
        return f"({str(self.e1)} {self.op.value} {str(self.e2)})"

    def accept_visitor(self, visitor):
        return visitor.binary(self.e1, self.op, self.e2)

class LetIn(namedtuple('LetIn', 'var e1 e2')):
    def __str__(self):
        return f"(let {self.var} := {str(self.e1)} in {str(self.e2)})"

    def accept_visitor(self, visitor):
        return visitor.let(self.var, self.e1, self.e2)
