fn main() {
    println!("Hello, world!");
}

type SudokuTable = [i16; 81];

pub fn initialize(input: &str) -> Option<SudokuTable> {
    let all: i16 = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1;
    let mut table: [i16; 81] = [all; 81];

    if input.len() != 81 {
        return None;
    }

    for (i, current_cell) in input.chars().enumerate() {
        table[i] = match current_cell {
            '0' => all,
            '1' => 1,
            '2' => 2,
            '3' => 4,
            '4' => 8,
            '5' => 16,
            '6' => 32,
            '7' => 64,
            '8' => 128,
            '9' => 256,
            _ => return None,
        };
    }

    return Some(table);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn initialize_invalid_character() {
        assert_eq!(
            initialize(
                "x00000000000000000000000000000000000000000000000000000000000000000000000000000000"
            ),
            None
        );
    }

    #[test]
    fn initialize_too_short() {
        assert_eq!(
            initialize(
                "04702000002190356600083000108057000090040030000320508000270003981036700000805400"
            ),
            None
        );
    }

    #[test]
    fn initialize_too_long() {
        assert_eq!(
            initialize(
                "0004702000002190356600083000108057000090040030000320508000270003981036700000805400"
            ),
            None
        );
    }

    #[test]
    fn initialize_all_zeroes() {
        let all: i16 = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1;

        assert_eq!(
            initialize(
                "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
            )
            .unwrap(),
            [all; 81]
        );
    }

    #[test]
    fn initialize_proper_puzzle() {
        let all: i16 = 256 + 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1;
        #[rustfmt::skip]
        let expected = 
            [all, all,   8,    64, all,   2,   all, all, all,
             all, all,   2,     1, 256, all,     4,  16,  32,
             32,  all, all,   all, 128,   4,   all, all, all,

             1,   all, 128,   all,  16,  64,   all, all, all,
             all, 256, all,   all,   8, all,   all,   4, all,
             all, all, all,     4,   2, all,    16, all, 128,

             all, all, all,     2,  64, all,   all, all,   4,
             256, 128,   1,   all,   4,  32,    64, all, all,
             all, all, all,   128, all,  16,     8, all, all];

        assert_eq!(
            initialize(
                "004702000002190356600083000108057000090040030000320508000270003981036700000805400"
            )
            .unwrap(),
            expected
        );
    }
}
