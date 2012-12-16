import unittest
from sudoku_utils import *

class TestSudoku(unittest.TestCase):
    def test_cell_could_contain__cell_is_locked_with_value__returns_value(self):
        cell = 0 + 0 + 0 + 0 + 0 + 0 + 4 + 0 + 0
        value = 4
        self.assertEqual(value, cell_could_contain(cell, value))

    def test_cell_could_contain__cell_is_locked_with_different_value__returns_zero(self):
        cell = 0 + 0 + 0 + 0 + 0 + 8 + 0 + 0 + 0
        value = 4
        self.assertEqual(0, cell_could_contain(cell, value))
    
    def test_cell_could_contain__cell_does_not_contain_value__returns_zero(self):
        cell = 256 + 128 + 64 + 32 + 0 + 8 + 4 + 2 + 1
        value = 16
        self.assertEqual(0, cell_could_contain(cell, value))

    def test_cell_could_contain__cell_contains_value__returns_value(self):
        cell = 256 + 128 + 64 + 32 + 0 + 8 + 4 + 2 + 1
        value = 8
        self.assertEqual(value, cell_could_contain(cell, value))
