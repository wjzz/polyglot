from __future__ import annotations # type: ignore

from enum import Enum
from typing import NamedTuple, NewType, List, TypeVar, Generic
from abc import ABC, abstractmethod
import unittest
from dataclasses import dataclass

class ArithOp(Enum):
    Add = "+"
    Sub = "-"
    Mul = "*"
    Div = "/"
    Mod = "%"

    def __str__(self):
        return self.value

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor[T]):
        ...

@dataclass(frozen=True)
class Lit(Expr):
    val: int

    def accept(self, visitor: ExprVisitor[T]):
        return visitor.visit_lit(self.val)

@dataclass(frozen=True)
class Binop(Expr):
    op: ArithOp
    left: Expr
    right: Expr

    def accept(self, visitor: ExprVisitor[T]):
        return visitor.visit_binop(self.op, self.left, self.right)

T = TypeVar("T")

class ExprVisitor(ABC, Generic[T]):
    @abstractmethod
    def visit_lit(self, val: int) -> T:
        ...

    @abstractmethod
    def visit_binop(self, op: ArithOp, left: Expr, right: Expr) -> T:
        ...

class Visitor(ExprVisitor[int]):
    def visit_lit(self, val) -> int:
        return val

    def visit_binop(self, op, left, right) -> int:
        l = left.accept(self)
        r = right.accept(self)
        if op == ArithOp.Add:
            return l + r
        else:
            raise NotImplementedError

def evaluate(e: Expr) -> int:
    return e.accept(Visitor())

class ExprTests(unittest.TestCase):
    def test_build(self):
        lit = Lit(123)
        add = Binop(ArithOp.Add, lit, lit)
        self.assertEqual(add.left, add.right)

    def test_evaluate(self):
        lit = Lit(123)
        add = Binop(ArithOp.Add, lit, lit)
        self.assertEqual(246, evaluate(add))
