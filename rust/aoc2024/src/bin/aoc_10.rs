use std::{
    collections::{HashMap, HashSet, VecDeque},
    str::FromStr,
    time::Instant,
};

use clap::{command, Parser};
use ndarray::Array2;

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_01.txt")]
    input: String,
}

#[derive(Debug, PartialEq, Eq, Clone)]
struct Input {
    map: Array2<u32>,
}

impl FromStr for Input {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let width = s.lines().nth(0).unwrap().len();
        let numbers: Vec<u32> = s.chars().filter_map(|x| x.to_digit(10)).collect();
        let height = numbers.len() / width;

        let map = Array2::from_shape_vec((width, height), numbers).unwrap();

        Ok(Input::new(map))
    }
}

impl Input {
    fn new(map: Array2<u32>) -> Self {
        Input { map }
    }
}

fn find(map: &Array2<u32>, number: u32) -> impl Iterator<Item = (usize, usize)> + '_ {
    let retval = map.indexed_iter().filter_map(move |((row, col), &value)| {
        if value == number {
            Some((row, col))
        } else {
            None
        }
    });

    retval
}

fn get_neigh<T>(array: &Array2<T>, row: usize, col: usize) -> Vec<(usize, usize)> {
    let shape = array.shape();
    let mut retval: Vec<(usize, usize)> = vec![];

    if row > 0 {
        retval.push((row - 1, col));
    }
    if row < shape[0] - 1 {
        retval.push((row + 1, col));
    }
    if col > 0 {
        retval.push((row, col - 1));
    }
    if col < shape[1] - 1 {
        retval.push((row, col + 1));
    }
    retval
}

struct Item {
    origin: (usize, usize),
    pos: (usize, usize),
}

fn solve1(input: &Input) -> usize {
    let mut origins: HashMap<(usize, usize), HashSet<(usize, usize)>> = HashMap::new();

    let mut queue: VecDeque<Item> = VecDeque::new();

    let (height, width) = input.map.dim();

    for row in 0..height {
        for col in 0..width {
            origins.insert((row, col), HashSet::new());
        }
    }

    for pos in find(&input.map, 9) {
        origins.get_mut(&pos).unwrap().insert(pos);
        queue.push_back(Item { origin: pos, pos });
    }

    while !queue.is_empty() {
        let item = queue.pop_front().unwrap();

        let value = input.map[item.pos];
        if value == 0 {
            continue;
        }
        for neigh_pos in get_neigh(&input.map, item.pos.0, item.pos.1) {
            let neigh_value = input.map[neigh_pos];
            if neigh_value == value - 1 {
                origins.get_mut(&neigh_pos).unwrap().insert(item.origin);
                queue.push_back(Item {
                    origin: item.origin,
                    pos: neigh_pos,
                });
            }
        }
    }

    find(&input.map, 0)
        .map(|pos| origins.get(&pos).unwrap().len())
        .sum()
}

fn solve2(input: &Input) -> usize {
    let mut counts: HashMap<(usize, usize), usize> = HashMap::new();

    let mut queue: VecDeque<(usize, usize)> = VecDeque::new();

    let (height, width) = input.map.dim();

    for row in 0..height {
        for col in 0..width {
            counts.insert((row, col), 0);
        }
    }

    for pos in find(&input.map, 9) {
        counts.insert(pos, 1);
        queue.push_back(pos);
    }

    while !queue.is_empty() {
        let pos = queue.pop_front().unwrap();

        let value = input.map[pos];
        if value == 0 {
            continue;
        }
        for neigh_pos in get_neigh(&input.map, pos.0, pos.1) {
            let neigh_value = input.map[neigh_pos];
            if neigh_value == value - 1 {
                counts.entry(neigh_pos).and_modify(|x| *x += 1);
                queue.push_back(neigh_pos);
            }
        }
    }

    find(&input.map, 0)
        .map(|pos| counts.get(&pos).unwrap())
        .sum()
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let start = Instant::now();
    let input: Input = data.parse().unwrap();
    println!("{}", solve1(&input));
    println!("{}", solve2(&input));
    let duration = start.elapsed();
    println!("Elapsed time: {} μs", duration.as_micros());
}

#[cfg(test)]
mod tests {
    use ndarray::array;

    use crate::{solve1, solve2, Input};

    fn get_sample_input() -> Input {
        Input::new(array![
            [8, 9, 0, 1, 0, 1, 2, 3],
            [7, 8, 1, 2, 1, 8, 7, 4],
            [8, 7, 4, 3, 0, 9, 6, 5],
            [9, 6, 5, 4, 9, 8, 7, 4],
            [4, 5, 6, 7, 8, 9, 0, 3],
            [3, 2, 0, 1, 9, 0, 1, 2],
            [0, 1, 3, 2, 9, 8, 0, 1],
            [1, 0, 4, 5, 6, 7, 3, 2]
        ])
    }

    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_10_sample.txt");

        let input: Input = input_str.parse().unwrap();

        assert_eq!(input, get_sample_input());
        assert_eq!(input.map.shape(), [8, 8]);
        assert_eq!(input.map.get((0, 2)).unwrap(), &0);
        assert_eq!(input.map.get((2, 0)).unwrap(), &8);
    }

    #[test]
    fn test_solve1() {
        let input = get_sample_input();
        assert_eq!(solve1(&input), 36);
    }

    #[test]
    fn test_solve2() {
        let input = get_sample_input();
        assert_eq!(solve2(&input), 81);
    }
}
