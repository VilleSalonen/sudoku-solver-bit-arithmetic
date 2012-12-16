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


def _lock_last_occurrences(table):
    previous_bits = [0] * 9
    possible_bits = [0] * 9

    # FIRST PASS: Find all possible values per box.
    for cell_ix in xrange(0, 81):
        box_ix = get_box_ix(cell_ix);

        # Step 1: What values in current cell have been found previously in this box? (previous_values & current_value)
        previously_used = previous_bits[box_ix] & table[cell_ix]

        # Step 2: Calculate used bits in current value by possible bits and previously used bits
        used_bits = possible_bits[box_ix] & previously_used

        # Step 3: Remove used bits from possible bits
        possible_bits[box_ix] ^= used_bits

        # Step 4: Find new bits from current value
        new_bits = table[cell_ix] ^ previously_used

        # Step 5: Add new bits to possible bits
        possible_bits[box_ix] ^= new_bits

        # Step 6: Add current bits to previously found bits
        previous_bits[box_ix] |= table[cell_ix]


    # SECOND PASS: Lock values if only one occurrence is found per box.
    for cell_ix in xrange(0, 81):
        box_ix = get_box_ix(cell_ix)
        if table[cell_ix] & possible_bits[box_ix]:
            table[cell_ix] &= possible_bits[box_ix]

    return table


def solve(table):
    solved_before = count_solved_numbers(table)
    solved_after = solved_before
    step = 1

    while (True):
        solved_before = solved_after

        table = _basic_elimination(table)
        table = _lock_last_occurrences(table)
        print "Step %d: %s" % (step, str(table))

        solved_after = count_solved_numbers(table)

        if (solved_before == solved_after):
            return table
        if (solved_after == 81):
            return table

        step += 1

    return table