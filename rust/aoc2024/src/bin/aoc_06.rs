use clap::{command, Parser};
use ndarray::{Array2, ArrayView};
use rayon::prelude::*;
use std::str::FromStr;

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_01.txt")]
    input: String,
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum LoopDetected {
    Yes,
    No,
}
#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Cell {
    Free,
    Taken,
    Walked,
}
#[derive(Debug, PartialEq, Eq, Clone)]
struct Map {
    matrix: Array2<Cell>,
    position: [usize; 2],
    past_directions: Array2<[i32; 2]>,
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum ParseError {
    InvalidChar,
    NoInitial,
}
impl Map {
    fn new(matrix: Array2<Cell>, position: [usize; 2]) -> Map {
        let past_directions = Array2::from_elem(matrix.raw_dim(), [0, 0]);
        Map {
            matrix,
            position,
            past_directions,
        }
    }
}
impl FromStr for Map {
    type Err = ParseError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let lines: Vec<&str> = s.lines().collect();
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
                    '^' => Ok(Cell::Walked),
                    '#' => Ok(Cell::Taken),
                    _ => Err(ParseError::InvalidChar),
                })
                .collect::<Result<Vec<Cell>, ParseError>>()?;

            matrix.push_row(ArrayView::from(&row)).unwrap();
        }

        let mut position: Option<[usize; 2]> = None;

        for ((row_idx, col_idx), &cell) in matrix.indexed_iter() {
            if cell == Cell::Walked {
                position = Some([row_idx, col_idx]);
                break;
            }
        }

        Ok(Map::new(matrix, position.ok_or(ParseError::NoInitial)?))
    }
}

fn walk(map: &mut Map) -> LoopDetected {
    let directions = [[-1, 0], [0, 1], [1, 0], [0, -1]];

    let mut iter_directions = directions.iter().cycle();

    let mut dir = iter_directions.next().unwrap();

    loop {
        let position = [map.position[0] as i32, map.position[1] as i32];
        map.matrix[map.position] = Cell::Walked;
        if map.past_directions[map.position] == *dir {
            return LoopDetected::Yes;
        }
        if map.past_directions[map.position] == [0, 0] {
            map.past_directions[map.position] = *dir;
        }

        let next_position = [position[0] + dir[0], position[1] + dir[1]];

        let exit: bool;
        let mut rotate = false;

        if next_position[0] < 0 || next_position[1] < 0 {
            exit = true;
        } else {
            let next_value = map
                .matrix
                .get((next_position[0] as usize, next_position[1] as usize));

            (rotate, exit) = match next_value {
                Some(Cell::Walked) => (false, false),
                Some(Cell::Taken) => (true, false),
                Some(Cell::Free) => (false, false),
                None => (false, true),
            };
        }

        if exit {
            break;
        }
        if rotate {
            dir = iter_directions.next().unwrap();
        } else {
            map.position = [next_position[0] as usize, next_position[1] as usize];
        }
    }

    // print_matrix(&map.matrix);
    LoopDetected::No
}

fn solve1(map: &mut Map) -> usize {
    let result = walk(map);
    assert!(result == LoopDetected::No, "Loop detected");

    print_matrix(&map.matrix);
    map.matrix.iter().filter(|&&x| x == Cell::Walked).count()
}

fn solve2(initial_map: &Map) -> usize {
    let mut initial_map_clone = initial_map.clone();

    let result = walk(&mut initial_map_clone);
    assert!(result == LoopDetected::No, "Loop detected");

    let walked_cells: Vec<[usize; 2]> = initial_map_clone
        .matrix
        .indexed_iter()
        .filter_map(|((row, col), &value)| match value {
            Cell::Walked if [row, col] != initial_map.position => Some([row, col]),
            _ => None,
        })
        .collect();

    walked_cells
        .par_iter()
        .map(|&pos| {
            let mut new_map = initial_map.clone();
            new_map.matrix[pos] = Cell::Taken;
            match walk(&mut new_map) {
                LoopDetected::Yes => 1,
                LoopDetected::No => 0,
            }
        })
        .sum()
}

fn print_matrix(matrix: &Array2<Cell>) {
    let char_array = matrix.mapv(|cell| match cell {
        Cell::Free => '.',
        Cell::Taken => '#',
        Cell::Walked => 'X',
    });

    for row in char_array.rows() {
        println!("{}", row.iter().collect::<String>());
    }
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let input: Map = data.parse().unwrap();

    println!("{}", solve1(&mut input.clone()));
    println!("{}", solve2(&input));
}
#[cfg(test)]
mod tests {
    use ndarray::array;

    use crate::solve1;
    use crate::solve2;
    use crate::Cell::*;

    use crate::Map;

    fn get_sample() -> Map {
        Map::new(
            array![
                [Free, Free, Free, Free, Taken, Free, Free, Free, Free, Free],
                [Free, Free, Free, Free, Free, Free, Free, Free, Free, Taken],
                [Free, Free, Free, Free, Free, Free, Free, Free, Free, Free],
                [Free, Free, Taken, Free, Free, Free, Free, Free, Free, Free],
                [Free, Free, Free, Free, Free, Free, Free, Taken, Free, Free],
                [Free, Free, Free, Free, Free, Free, Free, Free, Free, Free],
                [Free, Taken, Free, Free, Walked, Free, Free, Free, Free, Free],
                [Free, Free, Free, Free, Free, Free, Free, Free, Taken, Free],
                [Taken, Free, Free, Free, Free, Free, Free, Free, Free, Free],
                [Free, Free, Free, Free, Free, Free, Taken, Free, Free, Free]
            ],
            [6, 4],
        )
    }
    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_06_sample.txt");

        let map: Map = input_str.parse().unwrap();

        assert_eq!(map, get_sample());
    }
    #[test]
    fn test_solve1() {
        assert_eq!(solve1(&mut get_sample()), 41);
    }
    #[test]
    fn test_solve2() {
        assert_eq!(solve2(&get_sample()), 6);
    }
}
