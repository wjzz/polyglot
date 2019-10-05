from __future__ import annotations # type: ignore
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Optional, NamedTuple

x: int = 123
y = "123"
z = 'c'
z1: List[int] = []

class Example:
    def __init__(self, n: int):
        self.n = n

def check_example(ex: Example) -> int:
    return ex.n

# check_example(x)

@dataclass(frozen=True)
class BinaryTree():
    value: int
    left: Optional[BinaryTree]
    right: Optional[BinaryTree]

BTP = Optional[BinaryTree]

def size(tree: BTP) -> int:
    if tree is None:
        return 0
    else:
        return 1 + size(tree.left) + size(tree.right)