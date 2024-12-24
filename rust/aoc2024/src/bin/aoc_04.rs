use clap::{command, Parser};
use std::{collections::HashMap, str::FromStr};

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_04.txt")]
    input: String,
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Letter {
    X,
    M,
    A,
    S,
}
#[derive(Debug, PartialEq, Eq)]
struct Matrix {
    data: HashMap<(i64, i64), Letter>,
}

impl Matrix {
    const NEIGH_OFFSETS: [[[i64; 4]; 2]; 8] = [
        [[0, 1, 2, 3], [0, 0, 0, 0]],
        [[0, -1, -2, -3], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 1, 2, 3]],
        [[0, 0, 0, 0], [0, -1, -2, -3]],
        [[0, 1, 2, 3], [0, 1, 2, 3]],
        [[0, -1, -2, -3], [0, 1, 2, 3]],
        [[0, 1, 2, 3], [0, -1, -2, -3]],
        [[0, -1, -2, -3], [0, -1, -2, -3]],
    ];

    const X_NEIGH_OFFSETS: [[[i64; 3]; 2]; 4] = [
        [[-1, 0, 1], [-1, 0, 1]],
        [[1, 0, -1], [-1, 0, 1]],
        [[1, 0, -1], [1, 0, -1]],
        [[-1, 0, 1], [1, 0, -1]],
    ];

    fn get_offsets<I>(
        &self,
        row_idx: i64,
        col_idx: i64,
        row_offsets: I,
        col_offsets: I,
        size: usize,
    ) -> Option<Vec<Letter>>
    where
        I: Iterator<Item = i64>,
    {
        let values: Vec<Letter> = row_offsets
            .zip(col_offsets)
            .map(|(row_offset, col_offset)| {
                self.data.get(&(row_idx + row_offset, col_idx + col_offset))
            })
            .take_while(|x| x.is_some())
            .map(|x| x.unwrap())
            .copied()
            .collect();

        if values.len() == size {
            Some(values)
        } else {
            None
        }
    }
    fn get_neigh_letters(&self, row_idx: i64, col_idx: i64) -> Vec<Vec<Letter>> {
        let mut retval: Vec<Vec<Letter>> = vec![];

        for [row_offsets, col_offsets] in Self::NEIGH_OFFSETS {
            if let Some(letters) = self.get_offsets(
                row_idx,
                col_idx,
                row_offsets.into_iter(),
                col_offsets.into_iter(),
                4,
            ) {
                retval.push(letters);
            }
        }

        retval
    }
    fn get_x_neigh_letters(&self, row_idx: i64, col_idx: i64) -> Vec<Vec<Letter>> {
        let mut retval: Vec<Vec<Letter>> = vec![];

        for [row_offsets, col_offsets] in Self::X_NEIGH_OFFSETS {
            if let Some(letters) = self.get_offsets(
                row_idx,
                col_idx,
                row_offsets.into_iter(),
                col_offsets.into_iter(),
                3,
            ) {
                retval.push(letters);
            }
        }

        retval
    }
}

#[derive(Debug, PartialEq, Eq)]
struct InvalidCharError {
    char: char,
}
impl FromStr for Matrix {
    type Err = InvalidCharError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut data: HashMap<(i64, i64), Letter> = HashMap::new();

        for (row_idx, line) in s.lines().enumerate() {
            for (col_idx, char) in line.chars().enumerate() {
                let value = match char {
                    'X' => Letter::X,
                    'M' => Letter::M,
                    'A' => Letter::A,
                    'S' => Letter::S,
                    _ => return Err(InvalidCharError { char }),
                };

                data.insert((row_idx as i64, col_idx as i64), value);
            }
        }

        Ok(Matrix { data })
    }
}
fn solve1(m: &Matrix) -> usize {
    let mut retval = 0;
    for (&(row_idx, col_idx), &val) in m.data.iter() {
        if val == Letter::X {
            retval += m
                .get_neigh_letters(row_idx, col_idx)
                .iter()
                .filter(|x| **x == vec![Letter::X, Letter::M, Letter::A, Letter::S])
                .count();
        }
    }
    retval
}
fn solve2(m: &Matrix) -> usize {
    let mut retval = 0;
    for (&(row_idx, col_idx), &val) in m.data.iter() {
        if val == Letter::A {
            let counts = m
                .get_x_neigh_letters(row_idx, col_idx)
                .iter()
                .filter(|x| **x == vec![Letter::M, Letter::A, Letter::S])
                .count();
            if counts == 2 {
                retval += 1;
            }
        }
    }
    retval
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let matrix: Matrix = data.parse().unwrap();
    println!("{}", solve1(&matrix));
    println!("{}", solve2(&matrix));
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use crate::solve1;
    use crate::solve2;
    use crate::Letter::*;
    use crate::Matrix;

    fn get_sample_matrix() -> Matrix {
        Matrix {
            data: HashMap::from([
                ((2, 0), A),
                ((4, 9), M),
                ((1, 7), M),
                ((4, 2), A),
                ((4, 7), A),
                ((6, 7), X),
                ((4, 3), S),
                ((5, 1), X),
                ((5, 4), M),
                ((5, 9), A),
                ((7, 0), S),
                ((1, 3), M),
                ((5, 2), A),
                ((8, 4), M),
                ((6, 0), S),
                ((0, 6), M),
                ((8, 1), A),
                ((8, 7), M),
                ((6, 6), S),
                ((8, 9), M),
                ((9, 1), X),
                ((3, 0), M),
                ((9, 4), A),
                ((6, 8), S),
                ((4, 6), X),
                ((7, 2), X),
                ((8, 8), M),
                ((1, 5), M),
                ((3, 2), A),
                ((7, 4), M),
                ((2, 1), M),
                ((7, 7), A),
                ((9, 2), M),
                ((8, 6), M),
                ((6, 5), A),
                ((7, 8), A),
                ((4, 8), M),
                ((2, 2), X),
                ((8, 3), M),
                ((9, 0), M),
                ((6, 3), M),
                ((1, 2), A),
                ((3, 1), S),
                ((4, 0), X),
                ((1, 0), M),
                ((0, 2), M),
                ((5, 0), X),
                ((5, 5), X),
                ((3, 4), A),
                ((2, 6), A),
                ((5, 6), X),
                ((5, 8), M),
                ((1, 6), S),
                ((6, 1), M),
                ((7, 1), A),
                ((3, 5), S),
                ((7, 5), A),
                ((1, 9), A),
                ((0, 8), S),
                ((2, 5), M),
                ((6, 4), S),
                ((1, 1), S),
                ((3, 7), S),
                ((3, 8), M),
                ((9, 5), X),
                ((9, 7), A),
                ((2, 8), M),
                ((0, 1), M),
                ((2, 3), S),
                ((4, 1), M),
                ((9, 8), S),
                ((9, 9), X),
                ((8, 0), M),
                ((2, 7), A),
                ((1, 8), S),
                ((4, 4), A),
                ((7, 9), A),
                ((5, 7), A),
                ((0, 0), M),
                ((6, 9), S),
                ((3, 6), M),
                ((5, 3), M),
                ((8, 5), X),
                ((2, 9), M),
                ((3, 9), X),
                ((9, 3), X),
                ((9, 6), M),
                ((0, 4), X),
                ((7, 6), S),
                ((2, 4), X),
                ((4, 5), M),
                ((3, 3), M),
                ((0, 7), A),
                ((0, 5), X),
                ((6, 2), S),
                ((1, 4), X),
                ((7, 3), A),
                ((0, 3), S),
                ((0, 9), M),
                ((8, 2), M),
            ]),
        }
    }
    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_04_sample.txt");

        let m: Matrix = input_str.parse().unwrap();

        assert_eq!(m, get_sample_matrix(),);
    }

    #[test]
    fn test_offsets() {
        let m: Matrix = Matrix {
            data: HashMap::from([((10, 10), X), ((11, 10), M), ((12, 10), A), ((13, 11), S)]),
        };

        let offsets = m.get_offsets(
            10,
            10,
            [0, 1, 2, 3, 0].into_iter(),
            [0, 0, 0, 1, 0].into_iter(),
            5,
        );

        assert_eq!(offsets, Some(vec![X, M, A, S, X]),)
    }

    #[test]
    fn test_neigh() {
        let m: Matrix = get_sample_matrix();

        assert_eq!(
            m.get_neigh_letters(0, 0),
            vec![[M, M, A, M], [M, M, M, S], [M, S, X, M]]
        );

        /*
            MMMSXXMASM
            MSAMXMSMSA
            AMXSXMAAMM
            MSAMASMSMX
            XMASAMXAMM
            XXAMMXXAMA
            SMSMSASXSS
            SAXAMASAAA
            MAMMMXMMMM
            MXMXAXMASX
        */
        assert_eq!(
            m.get_neigh_letters(5, 5),
            vec![
                [X, A, A, X],
                [X, M, S, M],
                [X, X, A, M],
                [X, M, M, A],
                [X, S, A, M],
                [X, X, S, M],
                [X, S, A, M],
                [X, A, M, X]
            ]
        );
    }

    #[test]
    fn test_neigh_x() {
        let m: Matrix = get_sample_matrix();

        assert_eq!(
            m.get_x_neigh_letters(1, 2),
            vec![[M, A, S], [M, A, S], [S, A, M], [S, A, M]]
        );
    }
    #[test]
    fn test_solve1() {
        let m = get_sample_matrix();
        assert_eq!(solve1(&m), 18);
    }

    #[test]
    fn test_solve2() {
        let m = get_sample_matrix();
        assert_eq!(solve2(&m), 9);
    }

    // #[test]
    // fn test_solve2() {
    //     let input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
    //     assert_eq!(solve2(input), 48);
    // }
}
