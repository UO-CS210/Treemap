"""Unit tests for splitter.py"""

import unittest
from splitter import bisect

def show_pivot(i: int, li: list[int]) -> str:
    """String showing i"""
    return f"{sum(li)}= {sum(li[:i])}+{sum(li[i:])}  {li} => {li[:i]}|{li[i:]}"

class Tests(unittest.TestCase):
    def test_pair(self):
        """Special case for list of length 2"""
        li = [42, 42]
        parts = bisect(li)
        self.assertEqual(parts, ([42], [42]))

    def test_simple_units(self):
        li = [1, 1, 1, 1, 1, 1]
        left, right = bisect(li)
        self.assertEqual(left, [1, 1, 1])
        self.assertEqual(right, [1, 1, 1])

    def test_extreme_left(self):
        li = [12, 1, 1, 1]
        left, right = bisect(li)
        self.assertEqual(left, [12])
        self.assertEqual(right, [1, 1, 1])

    def test_extreme_right(self):
        li = [1, 1, 1, 12]
        parts = bisect(li)
        self.assertEqual(parts, ([1, 1, 1], [12]))

    def test_balanced_left(self):
        li = [3, 1, 1, 1]
        parts = bisect(li)
        self.assertEqual(parts, ([3], [1, 1, 1]))

    def test_balanced_right(self):
        li = [1, 1, 1, 3]
        parts = bisect(li)
        self.assertEqual(parts, ([1, 1, 1], [3]))

    def test_growing(self):
        li = [1, 2, 3, 4, 5, 6]  # total 21, target is 10, so [1..4] and [5..6]
        parts = bisect(li)
        self.assertEqual(parts, ([1, 2, 3, 4], [5, 6]))

    def test_shrinking(self):
        li = [6, 5, 4, 3, 2, 1]  # total 21, target is 10, so [6,5] and [4,3,2,1]
        parts = bisect(li)
        self.assertEqual(parts,  ([6, 5], [4, 3, 2, 1]))

if __name__ == "__main__":
    unittest.main()


