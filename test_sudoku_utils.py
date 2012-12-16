import unittest
from sudoku_utils import *

class SudokuUtilsTests(unittest.TestCase):
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


    def test_get_row_ix__first_cell__on_first_row(self):
        self.assertEqual(0, get_row_ix(0))

    def test_get_row_ix__last_cell__on_last_row(self):
        self.assertEqual(8, get_row_ix(80))

    def test_get_row_ix__from_middle__on_middle_row(self):
        self.assertEqual(4, get_row_ix(40))

    def test_get_row_ix__from_right_top_corner__on_first_row(self):
        self.assertEqual(0, get_row_ix(8))


    def test_get_box_ix__first_cell__in_first_box(self):
        self.assertEqual(0, get_box_ix(0))

    def test_get_box_ix__last_cell__in_last_box(self):
        self.assertEqual(8, get_box_ix(80))

    def test_get_box_ix__from_middle__on_middle_box(self):
        self.assertEqual(4, get_box_ix(40))

    def test_get_box_ix__from_right_top_corner__on_second_box(self):
        self.assertEqual(2, get_box_ix(8))


    def test_get_col_ix__first_cell__in_first_col(self):
        self.assertEqual(0, get_col_ix(0))

    def test_get_col_ix__last_cell__in_last_col(self):
        self.assertEqual(8, get_col_ix(80))

    def test_get_col_ix__from_middle__in_middle_col(self):
        self.assertEqual(4, get_col_ix(4))

    def test_get_col_ix__from_right_top_corner__in_last_col(self):
        self.assertEqual(8, get_col_ix(8))


    def test_initialize__valid_input__returns_valid_table(self):
        all = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1
        expected_table = [all, all,   4,   7, all,   2, all, all, all,
                          all, all,   2,   1,   9, all,   3,   5,   6,
                            6, all, all, all,   8,   3, all, all, all,

                            1, all,   8, all,   5,   7, all, all, all,
                          all,   9, all, all,   4, all, all,   3, all,
                          all, all, all,   3,   2, all,   5, all,   8,

                          all, all, all,   2,   7, all, all, all,   3,
                            9,   8,   1, all,   3,   6,   7, all, all,
                          all, all, all,   8, all,   5,   4, all, all]
        input = "004702000002190356600083000108057000090040030000320508000270003981036700000805400"
        table = initialize(input)
        self.assertEqual(expected_table, table)

