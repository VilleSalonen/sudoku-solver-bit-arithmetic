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
    
    
    def test_find_naked_pairs__two_naked_pairs__should_find_all(self):
        bit_table = [32,6,274,404,138,268,1,64,24,
                     64,7,275,276,10,32,128,284,24,
                     8,128,272,1,64,260,2,276,32,
                     3,43,3,64,16,128,256,41,4,
                     4,48,128,8,256,1,64,48,2,
                     256,25,64,32,4,2,24,25,128,
                     129,257,4,384,169,16,40,2,64,
                     145,65,8,2,161,68,52,144,256,
                     146,322,32,388,136,332,28,152,1]
        expected1 = { "value": 24, "box_ix": 2, "cell_ixs": [8, 17]}
        expected2 = { "value": 3, "box_ix": 3, "cell_ixs": [27, 29]}
        result = find_naked_pairs(bit_table)
        self.assertTrue(expected1 in result and expected2 in result)


    def test_eliminate_naked_pairs__two_naked_pairs__should_eliminate_naked_pair_candidates_from_other_cells_in_same_box(self):
        expected = [32,6,274,404,138,268,1,64,24,
                    64,7,275,276,10,32,128,260,24,
                    8,128,272,1,64,260,2,260,32,

                    3,40,3,64,16,128,256,41,4,
                    4,48,128,8,256,1,64,48,2,
                    256,24,64,32,4,2,24,25,128,

                    129,257,4,384,169,16,40,2,64,
                    145,65,8,2,161,68,52,144,256,
                    146,322,32,388,136,332,28,152,1]

        bit_table = [32,6,274,404,138,268,1,64,24,
                     64,7,275,276,10,32,128,284,24,
                     8,128,272,1,64,260,2,276,32,

                     3,43,3,64,16,128,256,41,4,
                     4,48,128,8,256,1,64,48,2,
                     256,25,64,32,4,2,24,25,128,

                     129,257,4,384,169,16,40,2,64,
                     145,65,8,2,161,68,52,144,256,
                     146,322,32,388,136,332,28,152,1]
        given_naked_pairs = [{ "value": 24, "box_ix": 2, "cell_ixs": [8, 17]}, { "value": 3, "box_ix": 3, "cell_ixs": [27, 29]}]
        result = eliminate_with_naked_pairs(bit_table, given_naked_pairs)
        self.assertEqual(expected, result)


    def test_line_lock_elimination__two_last_occurrences__should_lock_all(self):
        bit_table = [32,6,274,404,138,268,1,64,24,
                     64,7,275,276,10,32,128,260,24,
                     8,128,272,1,64,260,2,260,32,

                     3,40,3,64,16,128,256,41,4,
                     4,48,128,8,256,1,64,48,2,
                     256,24,64,32,4,2,24,25,128,

                     129,257,4,384,169,16,40,2,64,
                     145,65,8,2,161,68,52,144,256,
                     146,322,32,388,136,332,28,152,1]

        expected = [32,6,274,404,138,268,1,64,24,
                    64,7,275,276,10,32,128,260,24,
                    8,128,16,1,64,260,2,260,32,

                    3,40,3,64,16,128,256,41,4,
                    4,48,128,8,256,1,64,48,2,
                    256,24,64,32,4,2,24,1,128,

                    129,257,4,384,169,16,40,2,64,
                    145,65,8,2,161,68,52,144,256,
                    146,322,32,388,136,332,28,152,1]

        result = line_lock_elimination(bit_table)
        self.assertEqual(expected, result)

    def test_line_lock_elimination__two_last_occurrences_with_rotated_puzzle__should_lock_all(self):
        bit_table = [146, 145, 129,  256,   4,   3,    8,  64,  32,
                     322,  65, 257,   24,  48,  40,  128,   7,   6,
                     32,   8,    4,   64, 128,   3,  272, 275, 274,

                     388,   2, 384,   32,   8,  64,    1, 276, 404,
                     136, 161, 169,    4, 256,  16,   64,  10, 138,
                     332,  68,  16,    2,   1, 128,  260,  32, 268,

                     28,  52,  40,   24,  64, 256,    2, 128,   1,
                     152, 144,   2,   25,  48,  41,  260, 260,  64,
                     1, 256,  64,  128,   2,   4,   32,  24,  24]

        expected = [146, 145, 129,  256,   4,   3,    8,  64, 32,
                    322,  65, 257,   24,  48,  40,  128,   7,  6,
                    32,   8,    4,    64, 128,   3,   16, 275, 274,

                    388,   2, 384,   32,   8,  64,    1, 276, 404,
                    136, 161, 169,    4, 256,  16,   64,  10, 138,
                    332,  68,  16,    2,   1, 128,  260,  32, 268,

                    28,  52,  40,   24,  64, 256,    2, 128,   1,
                    152, 144,   2,    1,  48,  41,  260, 260,  64,
                    1, 256,  64,  128,   2,   4,   32,  24,  24]

        result = line_lock_elimination(bit_table)
        self.assertEqual(expected, result)


    def test_line_lock_elimination__locked_numbers_on_col_2__should_not_try_to_relock_already_locked_numbers(self):
        bit_table = [128,  64, 256,  214, 150, 212,   21,  32,   8,
                      32,   8, 208,    1, 148, 244,  256,   4,   2,
                       1,   4,  18,  256,   8,  48,   16,  64, 128,

                      16, 256,  32,    6,  64, 260,    8, 128,   1,
                      10, 128,  64,   30,   1,  28,    4, 256,  33,
                     266,   1,   4,  138,  32, 392,   64,   2,  16,

                      64,   2, 128,  168, 256,   1,  160,  16,   4,
                       4, 288,   8,  240, 144,   2,  160,   1, 320,
                     416,  16,   1,  228, 132, 196,    2,   8, 328]

        expected =  [128,  64, 256,  214,   2, 212,    1,  32,   8,
                      32,   8, 208,    1, 148, 244,  256,   4,   2,
                       1,   4,  18,  256,   8,  48,   16,  64, 128,

                      16, 256,  32,    6,  64, 260,    8, 128,   1,
                      10, 128,  64,   30,   1,  28,    4, 256,  33,
                     266,   1,   4,  138,  32, 392,   64,   2,  16,

                      64,   2, 128,  168, 256,   1,  160,  16,   4,
                       4, 288,   8,  240, 144,   2,  160,   1, 320,
                     416,  16,   1,  228, 132, 196,    2,   8, 328]

        result = line_lock_elimination(bit_table)
        self.assertEqual(expected, result)