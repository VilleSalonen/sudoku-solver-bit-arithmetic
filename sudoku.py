import sys

from sudoku_utils import *
from sudoku_logic import *

def solve_input(input):
    table = initialize(input)
    table = solve(table)
    print_human_table(table)

    return table


if __name__ == '__main__':
    solve_input(sys.argv[1])