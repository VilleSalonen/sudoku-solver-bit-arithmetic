from itertools import groupby
import operator

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


def find_naked_pairs(table):
    pairs = []

    for cell_ix in xrange(0, 81):
        box_ix = get_box_ix(cell_ix)

        if count_set_bits(table[cell_ix]) == 2:
            pairs.append({ "value": table[cell_ix], "cell_ix": cell_ix, "box_ix": box_ix })

    pairs_confirmed = []

    for box_ix in xrange(0, 81):
        pairs_in_this_box = [(pair["value"], pair) for pair in pairs if pair["box_ix"] == box_ix]

        pairs_grouped_by_value = groupby(pairs_in_this_box, operator.itemgetter(0))
        for key, items in pairs_grouped_by_value:
            bar1 = list(items)
            if len(bar1) == 2:
                pairs_confirmed.append(bar1)

    naked_pairs = []
    for pair_confirmed in pairs_confirmed:
        box_ix = pair_confirmed[0][1]["box_ix"]
        value = pair_confirmed[0][1]["value"]
        cell_ixs = [item[1]["cell_ix"] for item in pair_confirmed]
        naked_pairs.append({"box_ix": box_ix, "value": value, "cell_ixs": cell_ixs})

    return naked_pairs


def eliminate_with_naked_pairs(table, naked_pairs):
    table = list(table)

    for cell_ix in xrange(0, 81):
        box_ix = get_box_ix(cell_ix)
        for naked_pair in naked_pairs:
            if box_ix != naked_pair["box_ix"]:
                continue
            if cell_ix in naked_pair["cell_ixs"]:
                continue
            table[cell_ix] = table[cell_ix] ^ (table[cell_ix] & naked_pair["value"])

    return table


def line_lock_elimination(table):
    sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}

    NO_OCCURRENCES_FOUND_YET = -1
    MULTIPLE_OCCURRENCES_FOUND = -2

    table = list(table)

    valueCountsOnRow = {}
    valueCountsOnCol = {}

    for line_ix in xrange(0, 9):
        valueCountsOnRow[line_ix] = {}
        valueCountsOnCol[line_ix] = {}

        for value in xrange(1, 10):
            valueCountsOnRow[line_ix][value] = NO_OCCURRENCES_FOUND_YET
            valueCountsOnCol[line_ix][value] = NO_OCCURRENCES_FOUND_YET



    for cell_ix in xrange(0, 81):
        cells_row = get_row_ix(cell_ix)
        cells_col = get_col_ix(cell_ix)

        for value in xrange(1, 10):
            if count_set_bits(table[cell_ix]) == 1 and sudoku_to_bit_conversion[value] == table[cell_ix]:
                # If this number is already locked in this cell, it cannot be
                # found elsewhere on this row or column.
                if valueCountsOnRow[cells_row][value] != MULTIPLE_OCCURRENCES_FOUND:
                    valueCountsOnRow[cells_row][value] = MULTIPLE_OCCURRENCES_FOUND

                if valueCountsOnCol[cells_col][value] != MULTIPLE_OCCURRENCES_FOUND:
                    valueCountsOnCol[cells_col][value] = MULTIPLE_OCCURRENCES_FOUND

                continue

            # Number not found.
            if not cell_could_contain(table[cell_ix], sudoku_to_bit_conversion[value]):
                continue

            if valueCountsOnRow[cells_row][value] != MULTIPLE_OCCURRENCES_FOUND:
                if valueCountsOnRow[cells_row][value] == NO_OCCURRENCES_FOUND_YET:
                    valueCountsOnRow[cells_row][value] = cell_ix
                else:
                    valueCountsOnRow[cells_row][value] = MULTIPLE_OCCURRENCES_FOUND

            if valueCountsOnCol[cells_col][value] != MULTIPLE_OCCURRENCES_FOUND:
                if valueCountsOnCol[cells_col][value] == NO_OCCURRENCES_FOUND_YET:
                    valueCountsOnCol[cells_col][value] = cell_ix
                else:
                    valueCountsOnCol[cells_col][value] = MULTIPLE_OCCURRENCES_FOUND

    for i in xrange(0, 9):
        for value_ix in xrange(1, 10):
            if valueCountsOnCol[i][value_ix] >= 0:
                table[valueCountsOnCol[i][value_ix]] = sudoku_to_bit_conversion[value_ix]

            if valueCountsOnRow[i][value_ix] >= 0:
                table[valueCountsOnRow[i][value_ix]] = sudoku_to_bit_conversion[value_ix]

    return table


def find_hidden_sets(table):
    sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}

    value_counts_and_positions = {}
    for box_ix in xrange(0, 9):
        value_counts_and_positions[box_ix] = {}
        for value_ix in xrange(1, 10):
            value_counts_and_positions[box_ix][value_ix] = []

    for cell_ix in xrange(0, 81):
        box_ix = get_box_ix(cell_ix)
        for value_ix in xrange(1, 10):
            if cell_could_contain(table[cell_ix], sudoku_to_bit_conversion[value_ix]):
                value_counts_and_positions[box_ix][value_ix].append(cell_ix)

    matched = []

    for box_ix in xrange(0, 9):
        # Adapted from here: http://stackoverflow.com/questions/1241029/how-to-filter-a-dictionary-by-value
        sorted_data = sorted(value_counts_and_positions[box_ix].items(), key = lambda x: x[1])
        groups = groupby(sorted_data, key = lambda x: x[1])

        for key, group in groups:
            group = list(group)
            if len(group) != 1:
                matched.append((box_ix, dict(group)))

    result = []
    for x in matched:
        box_ix = x[0]

        # We're only interested in matches which have lists with length of 2.
        if len(x[1].items()[0][1]) != 2:
            continue

        values = [item[0] for item in x[1].items()]
        positions = x[1].items()[0][1]

        result.append({ "box_ix": box_ix, "values": sorted(values), "cell_ixs": sorted(positions) })

    return result


def eliminate_with_hidden_sets(table, hidden_sets):
    sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}

    for cell_ix in xrange(0, 81):
        for hidden_set in hidden_sets:
            box_ix = get_box_ix(cell_ix)

            if box_ix != hidden_set["box_ix"]:
                continue

            hidden_set_bit_value = sum([sudoku_to_bit_conversion[value] for value in hidden_set["values"]])

            if cell_ix in hidden_set["cell_ixs"]:
                table[cell_ix] = hidden_set_bit_value

    return table


def solve(table):
    solved_bits_before = count_set_bits_in_table(table)
    solved_bits_after = solved_bits_before

    while (True):
        solved_bits_before = solved_bits_after

        table = _basic_elimination(table)
        table = _lock_last_occurrences(table)
        table = line_lock_elimination(table)

        pair_locks = find_pair_locks(table)
        table = eliminate_with_pair_locks(table, pair_locks)

        naked_pairs = find_naked_pairs(table)
        table = eliminate_with_naked_pairs(table, naked_pairs)

        hidden_sets = find_hidden_sets(table)
        table = eliminate_with_hidden_sets(table, hidden_sets)

        solved_after = count_solved_numbers(table)
        solved_bits_after = count_set_bits_in_table(table)

        if (solved_bits_before == solved_bits_after):
            break
        if (solved_after == 81):
            break

    return table
