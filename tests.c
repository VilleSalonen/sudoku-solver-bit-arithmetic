#include <assert.h>
#include <stdbool.h>

#include "sudoku.h"

void cell_could_contain__all_values__all_values_possible() {
    unsigned short cell = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1;
    
    assert(cell_could_contain(cell, 1) && "Cell with all possible values should be able to contain all values!");
}

void cell_could_contain__locked_to_single__only_one_possible() {
    unsigned short cell = 256 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0;
    assert(cell_could_contain(cell, 9) && "Cell locked to single should containt that value!");
}

void cell_could_contain__locked_to_single__other_values_not_allowed() {
    unsigned short cell = 256 + 0 + 0 + 0 + 0 + 0 + 0 + 0 + 0;
    assert(cell_could_contain(cell, 1) == 0 && "Cell locked to single should not be able to contain other values!");
}

int main() {
    cell_could_contain__all_values__all_values_possible();
    cell_could_contain__locked_to_single__only_one_possible();
    cell_could_contain__locked_to_single__other_values_not_allowed();

	return 0;
}