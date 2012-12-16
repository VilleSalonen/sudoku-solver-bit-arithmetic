# Helpful supporting tables:
#
#     0  1  2  3  4  5  6  7  8     ----------------------------
#   ----------------------------    |        |        |        |
#  0| 0| 1| 2| 3| 4| 5| 6| 7| 8|    |   00   |   01   |   02   |
#  1| 9|10|11|12|13|14|15|16|17|    |        |        |        |
#  2|18|19|20|21|22|23|24|25|26|    ----------------------------
#   ----------------------------    |        |        |        |
#  3|27|28|29|30|31|32|33|34|35|    |   03   |   04   |   05   |
#  4|36|37|38|39|40|41|42|43|44|    |        |        |        |
#  5|45|46|47|48|49|50|51|52|53|    ----------------------------
#   ----------------------------    |        |        |        |
#  6|54|55|56|57|58|59|60|61|62|    |   06   |   07   |   08   |
#  7|63|64|65|66|67|68|69|70|71|    |        |        |        |
#  8|72|73|74|75|76|77|78|79|80|    ----------------------------
#   ----------------------------
#
# Sudoku value:  9   8   7   6   5   4   3   2   1
# Integer value: 256 128 64  32  16  8   4   2   1
# Bit value:     1   1   1   1   1   1   1   1   1
#
# If a cell can possibly contain 8, 7, 5 and 1:
#   Sudoku value: 987654321
#   Bit value:    011010001

def cell_could_contain(cell, value):
    return cell & value

def get_row_ix(cell_ix):
    return cell_ix / 9

def get_col_ix(cell_ix):
    return cell_ix % 9

def get_box_ix(cell_ix):
    return ((cell_ix / 3) % 3) + ((cell_ix / 27) * 3)

def initialize(input):
    all = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1
    sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}

    table = []
    for i in xrange(0, 81):
        table.append(0)

    length = len(input)
    for i in xrange(0, length):
        current_cell = input[i]
        cell_value = int(current_cell)
        if cell_value != 0:
            table[i] = sudoku_to_bit_conversion[cell_value]
        else:
            table[i] = all

    return table

def count_solved_numbers(table):
    numbers = 0
    for cell_ix in xrange(0, 81):
        if count_set_bits(table[cell_ix]) == 1:
            numbers += 1
    return numbers

def count_set_bits(input):
    amount = 0
    for i in xrange(0, 9):
        if (input & (1 << i)):
            amount += 1
    return amount

def convert_human_table_to_bit_table(table):
    sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}
    return [sudoku_to_bit_conversion[cell] for cell in table]