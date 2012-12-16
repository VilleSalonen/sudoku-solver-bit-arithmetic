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
        expected_table = [all, all,   8,    64, all,   2,   all, all, all,
                          all, all,   2,     1, 256, all,     4,  16,  32,
                          32, all, all,   all, 128,   4,   all, all, all,

                          1, all, 128,   all,  16,  64,   all, all, all,
                          all, 256, all,   all,   8, all,   all,   4, all,
                          all, all, all,     4,   2, all,    16, all, 128,

                          all, all, all,     2,  64, all,   all, all,   4,
                          256, 128,   1,   all,   4,  32,    64, all, all,
                          all, all, all,   128, all,  16,     8, all, all]
        input = "004702000002190356600083000108057000090040030000320508000270003981036700000805400"
        table = initialize(input)
        self.assertEqual(expected_table, table)


    def test_count_solved_numbers__easy_table__returns_solved_numbers(self):
        all = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1
        table = [all, all,   8,    64, all,   2,   all, all, all,
                 all, all,   2,     1, 256, all,     4,  16,  32,
                  32, all, all,   all, 128,   4,   all, all, all,

                   1, all, 128,   all,  16,  64,   all, all, all,
                 all, 256, all,   all,   8, all,   all,   4, all,
                 all, all, all,     4,   2, all,    16, all, 128,

                 all, all, all,     2,  64, all,   all, all,   4,
                 256, 128,   1,   all,   4,  32,    64, all, all,
                 all, all, all,   128, all,  16,     8, all, all]
        self.assertEqual(35, count_solved_numbers(table))


    def test_count_set_bits__no_bits__returns_zero(self):
        self.assertEqual(0, count_set_bits(0))

    def test_count_set_bits__all_bits__returns_all(self):
        all = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1
        self.assertEqual(9, count_set_bits(all))

    def test_count_set_bits__locked_value__returns_one(self):
        locked_value = 128
        self.assertEqual(1, count_set_bits(locked_value))


    def test_convert_human_table_to_bit_table(self):
        table = [3, 5, 4,  7, 6, 2,  9, 8, 1,
                 8, 7, 2,  1, 9, 4,  3, 5, 6,
                 6, 1, 9,  5, 8, 3,  2, 7, 4,

                 1, 3, 8,  9, 5, 7,  6, 4, 2,
                 2, 9, 5,  6, 4, 8,  1, 3, 7,
                 4, 6, 7,  3, 2, 1,  5, 9, 8,

                 5, 4, 6,  2, 7, 9,  8, 1, 3,
                 9, 8, 1,  4, 3, 6,  7, 2, 5,
                 7, 2, 3,  8, 1, 5,  4, 6, 9]
        expected_table = [  4,  16,   8,   64,  32,   2,  256, 128,   1,
                          128,  64,   2,    1, 256,   8,    4,  16,  32,
                           32,   1, 256,   16, 128,   4,    2,  64,   8,

                            1,   4, 128,  256,  16,  64,   32,   8,   2,
                            2, 256,  16,   32,   8, 128,    1,   4,  64,
                            8,  32,  64,    4,   2,   1,   16, 256, 128,

                           16,   8,  32,    2,  64, 256,  128,   1,   4,
                          256, 128,   1,    8,   4,  32,   64,   2,  16,
                           64,   2,   4,  128,   1,  16,    8,  32, 256]
        self.assertEqual(expected_table, convert_human_table_to_bit_table(table))
