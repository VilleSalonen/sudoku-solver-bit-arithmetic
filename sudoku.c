/**
 * Sudoku Solver using Bit Arithmetic
 * Author: Ville Salonen <ville.salonen@iki.fi>
 *
 * The idea is to implement Sudoku solver which solves the puzzles using
 * logical operations similar to how human would solve the puzzle. The tricky
 * thing is that these operations will mostly be implemented using bit
 * arithmetic.
 */

/**
 * Can cell contain number x? By definition, this function returns true for
 * multiple values in a single cell if the cell is not "locked down" to a single
 * value at the time.
 */
unsigned short cell_could_contain(unsigned short cell, unsigned short value) {
    return cell & (1 << (value - 1));
}