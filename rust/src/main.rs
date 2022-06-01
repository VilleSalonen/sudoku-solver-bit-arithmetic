fn main() {
    println!("Hello, world!");
}

pub fn initialize(input: &str) -> [i16; 81] {
    // all = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1
    // sudoku_to_bit_conversion = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256}
    //
    // table = []
    // for i in xrange(0, 81):
    //     table.append(0)
    //
    // length = len(input)
    // for i in xrange(0, length):
    //     current_cell = input[i]
    //     cell_value = int(current_cell)
    //     if cell_value != 0:
    //         table[i] = sudoku_to_bit_conversion[cell_value]
    //     else:
    //         table[i] = all
    //
    // return table
    let table: [i16; 81] = [0; 81];
    return table;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn initialize_all_zeroes() {
        assert_eq!(
            initialize(
                "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            ),
            [0; 81]
        );
    }
}
