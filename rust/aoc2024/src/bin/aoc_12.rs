use std::{
    collections::{HashSet, VecDeque},
    str::FromStr,
    time::Instant,
};

use clap::{command, Parser};
use ndarray::Array2;

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_12.txt")]
    input: String,
}

#[derive(Debug, PartialEq, Eq, Clone)]
struct Input {
    map: Array2<char>,
    regions: Vec<HashSet<(usize, usize)>>,
}
impl Input {
    fn new(map: Array2<char>) -> Self {
        let mut regions: Vec<HashSet<(usize, usize)>> = vec![];

        let mut walked: HashSet<(usize, usize)> = HashSet::new();

        let shape = map.shape();

        for row in 0..shape[0] {
            for col in 0..shape[1] {
                let pos = (row, col);
                if walked.contains(&pos) {
                    continue;
                }
                let region = walk(&map, pos);

                let mut region_vec: Vec<(usize, usize)> = region.iter().copied().collect();
                region_vec.sort();
                walked.extend(region.clone());
                regions.push(region);
            }
        }

        Self { map, regions }
    }

    fn get_pos_perimeter(&self, pos: &(usize, usize)) -> u32 {
        let region_char = *self.map.get(*pos).unwrap();
        get_neigh(&self.map, pos.0, pos.1)
            .iter()
            .map(|neigh| match neigh {
                Some(&ch) if ch != region_char => 1,
                Some(&_) => 0,
                None => 1,
            })
            .sum()
    }

    fn get_region_perimeter(&self, region: &HashSet<(usize, usize)>) -> u32 {
        let mut retval = 0;
        for pos in region.iter() {
            let p = self.get_pos_perimeter(pos);
            retval += p;
        }
        retval
    }
}

fn get_neigh<T>(array: &Array2<T>, row: usize, col: usize) -> Vec<Option<&T>> {
    let mut retval = vec![array.get((row + 1, col)), array.get((row, col + 1))];

    if row > 0 {
        retval.push(array.get((row - 1, col)));
    } else {
        retval.push(None);
    }

    if col > 0 {
        retval.push(array.get((row, col - 1)));
    } else {
        retval.push(None);
    }
    retval
}

fn get_neigh_indexed<T>(array: &Array2<T>, row: usize, col: usize) -> Vec<((usize, usize), &T)> {
    let shape = array.shape();
    let mut retval: Vec<((usize, usize), &T)> = vec![];

    if row > 0 {
        retval.push(((row - 1, col), array.get((row - 1, col)).unwrap()));
    }
    if row < shape[0] - 1 {
        retval.push(((row + 1, col), array.get((row + 1, col)).unwrap()));
    }
    if col > 0 {
        retval.push(((row, col - 1), array.get((row, col - 1)).unwrap()));
    }
    if col < shape[1] - 1 {
        retval.push(((row, col + 1), array.get((row, col + 1)).unwrap()));
    }
    retval
}

fn walk<T>(array: &Array2<T>, start_pos: (usize, usize)) -> HashSet<(usize, usize)>
where
    T: Eq,
{
    let mut queue: VecDeque<(usize, usize)> = VecDeque::from_iter([start_pos]);

    let start_element = array.get(start_pos).unwrap();

    let mut area: HashSet<(usize, usize)> = HashSet::new();

    while !queue.is_empty() {
        let pos = queue.pop_front().unwrap();
        if area.contains(&pos) {
            continue;
        }
        area.insert(pos);

        get_neigh_indexed(array, pos.0, pos.1)
            .iter()
            .for_each(|(pos, value)| {
                if *value == start_element && !area.contains(pos) {
                    queue.push_back(*pos)
                }
            });
    }
    area
}

impl FromStr for Input {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let width = s.lines().nth(0).unwrap().len();
        let chars: Vec<char> = s.chars().filter(|x| *x != '\n').collect();
        let height = chars.len() / width;

        let map = Array2::from_shape_vec((width, height), chars).unwrap();

        Ok(Input::new(map))
    }
}

fn solve1(input: &Input) -> u32 {
    input
        .regions
        .iter()
        .map(|region| region.len() as u32 * input.get_region_perimeter(region))
        .sum()
}

fn get_edges_of_vec(numbers: &Vec<u32>) -> Option<Vec<u32>> {
    if !numbers.is_sorted() {
        return None;
    }

    if numbers.is_empty() {
        None
    } else if numbers.len() == 1 {
        Some(vec![numbers[0], numbers[0]])
    } else {
        let mut retval: Vec<u32> = vec![numbers[0]];

        retval.extend(
            numbers
                .windows(2)
                .filter(|pair| {
                    if let [left, right] = pair {
                        right.abs_diff(*left) > 1
                    } else {
                        false
                    }
                })
                .flatten(),
        );
        retval.push(*numbers.last().unwrap());
        Some(retval)
    }
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let start = Instant::now();
    let input: Input = data.parse().unwrap();
    println!("{}", solve1(&input));
    // println!("{}", solve2(&input));
    let duration = start.elapsed();
    println!("Elapsed time: {} ms", duration.as_millis());
}

#[cfg(test)]
mod tests {
    use std::collections::{HashMap, HashSet};

    use ndarray::array;

    use crate::{get_edges_of_vec, solve1, walk, Input};

    fn get_sample_input() -> Input {
        Input::new(array![
            ['R', 'R', 'R', 'R', 'I', 'I', 'C', 'C', 'F', 'F'],
            ['R', 'R', 'R', 'R', 'I', 'I', 'C', 'C', 'C', 'F'],
            ['V', 'V', 'R', 'R', 'R', 'C', 'C', 'F', 'F', 'F'],
            ['V', 'V', 'R', 'C', 'C', 'C', 'J', 'F', 'F', 'F'],
            ['V', 'V', 'V', 'V', 'C', 'J', 'J', 'C', 'F', 'E'],
            ['V', 'V', 'I', 'V', 'C', 'C', 'J', 'J', 'E', 'E'],
            ['V', 'V', 'I', 'I', 'I', 'C', 'J', 'J', 'E', 'E'],
            ['M', 'I', 'I', 'I', 'I', 'I', 'J', 'J', 'E', 'E'],
            ['M', 'I', 'I', 'I', 'S', 'I', 'J', 'E', 'E', 'E'],
            ['M', 'M', 'M', 'I', 'S', 'S', 'J', 'E', 'E', 'E']
        ])
    }

    #[test]
    fn test_region_perimeter() {
        let input = get_sample_input();
        let perimeter = input.get_region_perimeter(&input.regions[0]);
        assert_eq!(perimeter, 18);
    }

    #[test]
    fn test_solve1() {
        let input = get_sample_input();
        assert_eq!(solve1(&input), 1930);
    }

    #[test]
    fn test_walk1() {
        let input = get_sample_input();
        assert_eq!(
            walk(&input.map, (0, 0)),
            HashSet::from_iter([
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (2, 2),
                (2, 3),
                (2, 4),
                (3, 2),
            ])
        );
    }
    #[test]
    fn test_walk2() {
        let input = get_sample_input();
        assert_eq!(
            walk(&input.map, (9, 9)),
            HashSet::from_iter([
                (4, 9),
                (5, 8),
                (5, 9),
                (6, 8),
                (6, 9),
                (7, 8),
                (7, 9),
                (8, 7),
                (8, 8),
                (8, 9),
                (9, 7),
                (9, 8),
                (9, 9),
            ])
        );
    }

    #[test]
    fn test_get_edges_of_vec() {
        assert_eq!(get_edges_of_vec(&vec![1, 2, 3, 4]), Some(vec![1, 4]));
        assert_eq!(get_edges_of_vec(&vec![]), None);
        assert_eq!(get_edges_of_vec(&vec![5]), Some(vec![5, 5]));

        assert_eq!(get_edges_of_vec(&vec![5, 6, 8, 9]), Some(vec![5, 6, 8, 9]));
        assert_eq!(
            get_edges_of_vec(&vec![2, 3, 4, 5, 6, 8, 9, 10, 11]),
            Some(vec![2, 6, 8, 11])
        );

        assert_eq!(
            get_edges_of_vec(&vec![1, 2, 5, 6, 8, 9]),
            Some(vec![1, 2, 5, 6, 8, 9])
        );
        assert_eq!(get_edges_of_vec(&vec![1, 2, 10, 5, 6, 8, 9]), None);
    }
    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_12_sample.txt");
        let input: Input = input_str.parse().unwrap();

        assert_eq!(input, get_sample_input());

        let expected = vec![
            HashSet::from([
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (2, 2),
                (2, 3),
                (2, 4),
                (3, 2),
            ]),
            HashSet::from([(0, 4), (1, 5), (1, 4), (0, 5)]),
            HashSet::from([
                (5, 4),
                (3, 3),
                (2, 5),
                (4, 4),
                (6, 5),
                (2, 6),
                (0, 6),
                (1, 8),
                (1, 6),
                (0, 7),
                (3, 4),
                (1, 7),
                (5, 5),
                (3, 5),
            ]),
            HashSet::from([
                (3, 7),
                (4, 8),
                (0, 8),
                (0, 9),
                (1, 9),
                (2, 9),
                (3, 9),
                (2, 8),
                (3, 8),
                (2, 7),
            ]),
            HashSet::from([
                (4, 3),
                (5, 0),
                (4, 1),
                (5, 3),
                (6, 0),
                (4, 2),
                (5, 1),
                (2, 0),
                (2, 1),
                (4, 0),
                (3, 0),
                (3, 1),
                (6, 1),
            ]),
            HashSet::from([
                (6, 6),
                (3, 6),
                (5, 6),
                (8, 6),
                (7, 6),
                (4, 6),
                (5, 7),
                (4, 5),
                (6, 7),
                (7, 7),
                (9, 6),
            ]),
            HashSet::from([(4, 7)]),
            HashSet::from([
                (5, 9),
                (9, 8),
                (5, 8),
                (7, 9),
                (7, 8),
                (9, 9),
                (6, 8),
                (8, 7),
                (6, 9),
                (4, 9),
                (8, 9),
                (9, 7),
                (8, 8),
            ]),
            HashSet::from([
                (6, 2),
                (8, 5),
                (8, 2),
                (7, 1),
                (7, 4),
                (7, 2),
                (8, 1),
                (6, 3),
                (8, 3),
                (9, 3),
                (7, 5),
                (6, 4),
                (5, 2),
                (7, 3),
            ]),
            HashSet::from([(9, 1), (9, 0), (9, 2), (8, 0), (7, 0)]),
            HashSet::from([(8, 4), (9, 4), (9, 5)]),
        ];

        assert_eq!(input.regions, expected);
    }
}
