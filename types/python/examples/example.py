from __future__ import annotations

from collections import namedtuple
from typing import NamedTuple
import unittest

class Point(NamedTuple):
    x: float
    y: float

    def swap(self) -> Point:
        return Point(x = self.y, y = self.x)

    def __add__(self: Point, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    # def __eq__(self: Point, other: Point) -> bool:
    #     return id(self) == id(other)

class PointTests(unittest.TestCase):
    def test_init(self):
        p = Point(1, 2)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
    
    def test_add(self):
        p1 = Point(1, 5)
        p2 = Point(4, 10)
        p3 = p1 + p2
        self.assertEqual(5, p3.x)
        self.assertEqual(15, p3.y)

    def test_eq(self):
        p1 = Point(1, 0)
        p2 = Point(1, 0)
        p3 = Point(0, 1)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
