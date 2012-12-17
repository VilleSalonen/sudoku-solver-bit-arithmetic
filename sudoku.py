import sys

from sudoku_utils import *
from sudoku_logic import *

def solve_input(input):
    table = initialize(input)

    original_locked_numbers = count_solved_numbers(table)
    table = solve(table)
    solved_numbers = count_solved_numbers(table)

    if solved_numbers == 81:
        print_human_table(table)
    else:
        print "Originally %d locked numbers" % (original_locked_numbers)
        print "In the end %d solved numbers" % (solved_numbers)
        print_bit_table(table)
        print_table(table)

    return table


if __name__ == '__main__':
    solve_input(sys.argv[1])