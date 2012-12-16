from sudoku_utils import *
from sudoku_logic import *

def solve_input(input):
    table = initialize(input)
    table = solve(table)
    return table