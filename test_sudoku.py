import unittest
from sudoku import *

class SudokuTests(unittest.TestCase):
    def test_solve__easy_input__returns_solved(self):
        # Source: http://www.websudoku.com/?level=1&set_id=10206368615
        expected_table = [8, 7, 9,  3, 2, 5,  1, 6, 4,
                          6, 4, 5,  1, 8, 7,  9, 3, 2,
                          1, 3, 2,  9, 4, 6,  5, 7, 8,

                          5, 9, 6,  2, 7, 3,  4, 8, 1,
                          2, 8, 7,  5, 1, 4,  3, 9, 6,
                          4, 1, 3,  8, 6, 9,  7, 2, 5,

                          7, 2, 8,  4, 9, 1,  6, 5, 3,
                          3, 6, 4,  7, 5, 2,  8, 1, 9,
                          9, 5, 1,  6, 3, 8,  2, 4, 7]
        expected_table = convert_human_table_to_bit_table(expected_table)
        easy_input = "009000060040100902130940078506070480080000090013060705720091053304002010050000200"
        self.assertEqual(expected_table, solve_input(easy_input))

    def test_solve__medium_input__returns_solved(self):
        expected_table = [2, 5, 9,  6, 4, 1,  3, 7, 8,
                          7, 6, 4,  2, 8, 3,  1, 5, 9,
                          8, 3, 1,  9, 5, 7,  6, 4, 2,

                          9, 4, 6,  8, 3, 2,  5, 1, 7,
                          1, 2, 3,  5, 7, 6,  8, 9, 4,
                          5, 8, 7,  4, 1, 9,  2, 3, 6,

                          3, 9, 8,  1, 2, 4,  7, 6, 5,
                          4, 7, 2,  3, 6, 5,  9, 8, 1,
                          6, 1, 5,  7, 9, 8,  4, 2, 3]
        expected_table = convert_human_table_to_bit_table(expected_table)
        medium_input = "259000000000003009000957040940000507120000094507000036090124000400300000000000423"
        self.assertEqual(expected_table, solve_input(medium_input))

    def test_solve__hard_input__returns_solved(self):
        # Source: http://www.websudoku.com/?level=3&set_id=6530973795
        expected_table = [5, 4, 3,  8, 1, 7,  9, 6, 2,
                          6, 8, 7,  2, 5, 9,  1, 3, 4,
                          9, 1, 2,  6, 3, 4,  5, 8, 7,
                          1, 2, 6,  3, 9, 8,  4, 7, 5,
                          7, 3, 4,  5, 2, 1,  6, 9, 8,
                          8, 9, 5,  7, 4, 6,  3, 2, 1,
                          3, 7, 8,  4, 6, 5,  2, 1, 9,
                          4, 6, 9,  1, 8, 2,  7, 5, 3,
                          2, 5, 1,  9, 7, 3,  8, 4, 6]
        expected_table = convert_human_table_to_bit_table(expected_table)
        hard_input = "003007060600250000900000080020300070004501600090006020070000009000082003050900800"
        self.assertEqual(expected_table, solve_input(hard_input))

    def test_solve__evil_input__returns_solved(self):
        # Source: http://www.websudoku.com/?level=4&set_id=9279274439
        expected_table = [  6, "?", "?",  "?", "?", "?",    1,   7, "?",
                            7, "?", "?",  "?", "?",   6,    8, "?", "?",
                            4,   8,   5,    1,   7, "?",    2, "?",   6,

                          "?", "?", "?",    7,   5,   8,    9, "?",   3,
                            3, "?",   8,    4,   9,   1,    7, "?",   2,
                            9, "?",   7,    6,   3,   2,  "?",   1,   8,

                          "?", "?",   3,  "?", "?",   5,  "?",   2,   7,
                          "?", "?",   4,    2, "?", "?",  "?", "?",   9,
                          "?", "?",   6,  "?", "?", "?",  "?", "?",   1]
        evil_input = "600000100700006800480100200000708003000401000900602000003005027004200009006000001"
        bit_table = solve_input(evil_input)
        self.assertEqual(expected_table, convert_bit_table_to_human_table(bit_table))