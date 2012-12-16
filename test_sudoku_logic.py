import unittest
from sudoku_logic import *

class SudokuLogicTests(unittest.TestCase):
    def test_find_pair_locks__locked_pair_available__returns_value_and_position(self):
        # This is the solved version after applying basic_elimination and
        # lock_last_occurrences to http://www.websudoku.com/?level=4&set_id=9279274439
        bit_table = [ 32, 278, 274,  404, 478, 332,    1, 348,  24,
                      64, 279, 275,  276, 286,  32,  128, 284,  24,
                       8, 128, 272,    1, 340, 324,    2, 372,  48,

                      19,  59,  19,   64, 272, 128,  312, 313,   4,
                     148, 116, 208,    8, 276,   1,  368, 496,   2,
                     256,  93, 209,   32,  20,   2,   88, 217, 152,

                     129, 257,   4,  384, 425,  16,   40,   2,  64,
                     145,  81,   8,    2, 229,  68,   52, 180, 256,
                     146, 338,  32,  388, 460, 332,   28, 156,   1]
        expected = { "value": 3, "box": 0, "cell_ixs": [1, 10], "col": 1, "row": -1 }
        result = find_pair_locks(bit_table)
        self.assertEqual(17, len(result))
        self.assertEqual(True, expected in result)

    def test_find_pair_locks__pair_candidate_but_locked_number_in_same_box__should_not_suggest_that_candidate(self):
        # Box 2 contains possible 7 values in cells 6 and 24 but this should not
        # be suggested as a pair candidate because the same box has a locked 7
        # in cell 26.
        bit_table = [ 12,   1,  12,    2, 128,  76,  104,  16, 256,
                      64, 260,  16,  312, 296,  28,   42, 138,   1,
                      32, 128,   2,  280, 328,   1,   72,   4,  64,
                      29,  32,  64,  128,  11, 256,   22,   2,   4,
                     128,   2,  17,   49,   4,  16,   64, 256,   8,
                     284, 260, 284,   64,  42,  26,  128,   1,  36,
                     256,  16, 384,    4, 328, 200,    1,  32,   2,
                     261,  64,  32,  393, 331, 202,  268, 136,  16,
                       2,   8, 389,  385,  16,  32,  260,  64, 132]
        expected_fail = { "value": 7, "box": 2, "cell_ixs": [6, 24], "col": 6, "row": -1 }
        result = find_pair_locks(bit_table)
        self.assertEqual(False, expected_fail in result)


    def test_eliminate_with_pair_locks__one_pair_lock__should_eliminate(self):
        bit_table = [ 32, 278, 274,  404, 478, 332,    1, 348,  24,
                      64, 279, 275,  276, 286,  32,  128, 284,  24,
                       8, 128, 272,    1, 340, 324,    2, 372,  48,

                       19,  59,  19,   64, 272, 128,  312, 313,   4,
                      148, 116, 208,    8, 276,   1,  368, 496,   2,
                      256,  93, 209,   32,  20,   2,   88, 217, 152,

                      129, 257,   4,  384, 425,  16,   40,   2,  64,
                      145,  81,   8,    2, 229,  68,   52, 180, 256,
                      146, 338,  32,  388, 460, 332,   28, 156,   1]
        expected_table = [ 32, 278, 274,  404, 478, 332,    1, 348,  24,
                           64, 279, 275,  276, 286,  32,  128, 284,  24,
                            8, 128, 272,    1, 340, 324,    2, 372,  48,

                           19,  59,  19,   64, 272, 128,  312, 313,   4,
                          148, 112, 208,    8, 276,   1,  368, 496,   2,
                          256,  89, 209,   32,  20,   2,   88, 217, 152,

                          129, 257,   4,  384, 425,  16,   40,   2,  64,
                          145,  81,   8,    2, 229,  68,   52, 180, 256,
                          146, 338,  32,  388, 460, 332,   28, 156,   1]
        self.assertEqual(expected_table, eliminate_with_pair_locks(bit_table, [{ "value": 3, "box": 0, "cell_ixs": [1, 10], "col": 1, "row": -1 }]))