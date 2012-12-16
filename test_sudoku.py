import unittest
from sudoku import *

class SudokuTests(unittest.TestCase):
    def test_solve__easy_input__returns_solved(self):
        expected_table = [3, 5, 4,  7, 6, 2,  9, 8, 1,
                          8, 7, 2,  1, 9, 4,  3, 5, 6,
                          6, 1, 9,  5, 8, 3,  2, 7, 4,

                          1, 3, 8,  9, 5, 7,  6, 4, 2,
                          2, 9, 5,  6, 4, 8,  1, 3, 7,
                          4, 6, 7,  3, 2, 1,  5, 9, 8,

                          5, 4, 6,  2, 7, 9,  8, 1, 3,
                          9, 8, 1,  4, 3, 6,  7, 2, 5,
                          7, 2, 3,  8, 1, 5,  4, 6, 9]
        expected_table = convert_human_table_to_bit_table(expected_table)
        easy_input = "004702000002190356600083000108057000090040030000320508000270003981036700000805400"
        self.assertEqual(expected_table, solve_input(easy_input))