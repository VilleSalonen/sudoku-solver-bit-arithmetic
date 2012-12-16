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

def find_pair_locks(bit_table):
    sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}

    box_candidate_pairs = []
    for i in xrange(0, 9):
        box_candidate_pairs.append({1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []})

    for cell_ix in xrange(0, 81):
        cell = bit_table[cell_ix]
        if count_set_bits(cell) == 1:
            continue

        box_ix = get_box_ix(cell_ix)

        for value in xrange(1, 10):
            bit_value = sudoku_to_bit_conversion[value]
            if cell_could_contain(cell, bit_value):
                box_candidate_pairs[box_ix][value].append(cell_ix)

    candidate_pairs = []
    for i in xrange(0, 9):
        for k in xrange(1, 10):
            candidate_pair = box_candidate_pairs[i][k]
            if len(candidate_pair) == 2:
                value = k
                box = get_box_ix(candidate_pair[0])

                first_col_ix = get_col_ix(candidate_pair[0])
                first_row_ix = get_row_ix(candidate_pair[0])
                second_col_ix = get_col_ix(candidate_pair[1])
                second_row_ix = get_row_ix(candidate_pair[1])

                if (first_col_ix == second_col_ix):
                    row = -1
                    col = first_col_ix
                elif (first_row_ix == second_row_ix):
                    row = first_row_ix
                    col = -1
                else:
                    # Pair is not on same row or column so it cannot be used
                    continue

                candidate_pairs.append({ "value": k, "box": box, "cell_ixs": candidate_pair, "row": row, "col": col })

    return candidate_pairs


def eliminate_with_pair_locks(table, pair_locks):
    sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}

    for cell_ix in xrange(0, 81):
        row_ix = get_row_ix(cell_ix)
        col_ix = get_col_ix(cell_ix)
        box_ix = get_box_ix(cell_ix)

        for pair_lock in pair_locks:
            if pair_lock["box"] == box_ix:
                # Don't eliminate from the same box where pair lock was found
                continue

            if pair_lock["row"] != -1 and pair_lock["row"] == row_ix:
                table[cell_ix] ^= (table[cell_ix] & sudoku_to_bit_conversion[pair_lock["value"]])
                continue
            if pair_lock["col"] != -1 and pair_lock["col"] == col_ix:
                table[cell_ix] ^= (table[cell_ix] & sudoku_to_bit_conversion[pair_lock["value"]])
                continue

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