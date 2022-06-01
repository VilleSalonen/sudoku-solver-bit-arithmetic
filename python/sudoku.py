import sys

from sudoku_utils import *
from sudoku_logic import *

def solve_input(input):
    table = initialize(input)
    table = solve(table)
    return table

if __name__ == '__main__':
    print_human_table(solve_input(sys.argv[1]))