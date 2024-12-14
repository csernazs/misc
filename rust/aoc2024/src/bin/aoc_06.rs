use std::str::FromStr;

use clap::{command, Parser};
use ndarray::{Array2, ArrayView};

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_01.txt")]
    input: String,
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Cell {
    Free,
    Taken,
    Initial,
    Walked,
}
struct Map {
    matrix: Array2<Cell>,
    position: [usize; 2],
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum ParseError {
    InvalidChar,
    NoInitial,
}

impl FromStr for Map {
    type Err = ParseError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let lines: Vec<&str> = s.lines().collect();
        let no_rows = lines.len();
        let no_cols = lines[0].len();

        let mut matrix: Array2<Cell> = Array2::from_elem((0, no_cols), Cell::Free);
        for line in s.lines() {
            if line.is_empty() {
                continue;
            }
            let row: Vec<Cell> = line
                .chars()
                .map(|c| match c {
                    '.' => Ok(Cell::Free),
                    '^' => Ok(Cell::Initial),
                    '#' => Ok(Cell::Taken),
                    _ => Err(ParseError::InvalidChar),
                })
                .collect::<Result<Vec<Cell>, ParseError>>()?;

            matrix.push_row(ArrayView::from(&row)).unwrap();
        }

        let mut position: Option<[usize; 2]> = None;

        for ((row_idx, col_idx), &cell) in matrix.indexed_iter() {
            if cell == Cell::Initial {
                position = Some([row_idx, col_idx]);
                break;
            }
        }

        Ok(Map {
            matrix,
            position: position.ok_or(ParseError::NoInitial)?,
        })
    }
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let input: Map = data.parse().unwrap();

    // println!("{}", solve1(&input));
    // println!("{}", solve2(&input));
}
#[cfg(test)]
mod tests {
    #[test]
    fn test_parse() {}
}
