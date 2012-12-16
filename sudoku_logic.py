from sudoku_utils import *

def _basic_elimination(table):
    rows = [511] * 9
    cols = [511] * 9
    boxes = [511] * 9

    # FIRST PASS: Find numbers for elimination
    for cell_ix in xrange(0, 81):
        if _no_definite_value_in_cell(table[cell_ix]):
            continue

        row_ix = get_row_ix(cell_ix)
        col_ix = get_col_ix(cell_ix)
        box_ix = get_box_ix(cell_ix)

        rows[row_ix]  ^= table[cell_ix]
        cols[col_ix]  ^= table[cell_ix]
        boxes[box_ix] ^= table[cell_ix]

    # SECOND PASS: Eliminate numbers
    for cell_ix in xrange(0, 81):
        if _locked_value_in_cell(table[cell_ix]):
            continue

        row_ix = get_row_ix(cell_ix)
        col_ix = get_col_ix(cell_ix)
        box_ix = get_box_ix(cell_ix)

        table[cell_ix] &= rows[row_ix]
        table[cell_ix] &= cols[col_ix]
        table[cell_ix] &= boxes[box_ix]

    return table

def _no_definite_value_in_cell(cell):
    return count_set_bits(cell) != 1

def _locked_value_in_cell(cell):
    return count_set_bits(cell) == 1

def solve(table):
    solved_before = count_solved_numbers(table)
    solved_after = solved_before
    step = 1

    while (True):
        solved_before = solved_after

        table = _basic_elimination(table)
        print "Step %d: %s" % (step, str(table))

        solved_after = count_solved_numbers(table)

        if (solved_before == solved_after):
            return table
        if (solved_after == 81):
            return table

        step += 1

    return table