use std::{
    collections::{HashMap, HashSet},
    str::FromStr,
};

use clap::{command, Parser};
use itertools::Itertools;

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_07.txt")]
    input: String,
}

struct Input {
    antennas: HashMap<char, Vec<[i32; 2]>>,
    positions: HashMap<[i32; 2], char>,
    width: usize,
    height: usize,
}

impl Input {
    fn new(antennas: HashMap<char, Vec<[i32; 2]>>, width: usize, height: usize) -> Self {
        let mut positions: HashMap<[i32; 2], char> = HashMap::new();

        for (&character, pos_vec) in antennas.iter() {
            for &pos in pos_vec {
                positions.insert(pos, character);
            }
        }
        Input {
            antennas,
            positions,
            width,
            height,
        }
    }
}
impl FromStr for Input {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut antennas: HashMap<char, Vec<[i32; 2]>> = HashMap::new();

        let lines: Vec<&str> = s.lines().collect();

        for (row_idx, line) in lines.iter().enumerate() {
            for (col_idx, char) in line.chars().enumerate() {
                if char == '.' {
                    continue;
                }
                antennas
                    .entry(char)
                    .and_modify(|x| x.push([row_idx as i32, col_idx as i32]))
                    .or_insert(vec![[row_idx as i32, col_idx as i32]]);
            }
        }
        Ok(Input::new(antennas, lines[0].len(), lines.len()))
    }
}

fn calculate_antinodes1(pos1: &[i32; 2], pos2: &[i32; 2]) -> [[i32; 2]; 2] {
    let row_diff = pos1[0] - pos2[0];
    let col_diff = pos1[1] - pos2[1];
    // dbg!(row_diff);
    // dbg!(col_diff);
    let node1_pos = [pos1[0] + row_diff, pos1[1] + col_diff];
    let node2_pos = [pos2[0] - row_diff, pos2[1] - col_diff];

    [node1_pos, node2_pos]
}

fn calculate_antinodes2(
    pos1: &[i32; 2],
    pos2: &[i32; 2],
    width: usize,
    height: usize,
) -> Vec<[i32; 2]> {
    let row_diff = pos1[0] - pos2[0];
    let col_diff = pos1[1] - pos2[1];
    // dbg!(row_diff);
    // dbg!(col_diff);

    let mut retval: Vec<[i32; 2]> = vec![];

    let mut next_node = *pos1;

    let max_height = height as i32 - 1;
    let max_width = width as i32 - 1;
    loop {
        next_node[0] += row_diff;
        next_node[1] += col_diff;

        if next_node[0] < 0
            || next_node[1] < 0
            || next_node[0] > max_height
            || next_node[1] > max_width
        {
            break;
        }
        retval.push(next_node);
    }

    next_node = *pos2;

    loop {
        next_node[0] -= row_diff;
        next_node[1] -= col_diff;

        if next_node[0] < 0
            || next_node[1] < 0
            || next_node[0] > max_height
            || next_node[1] > max_width
        {
            break;
        }
        retval.push(next_node);
    }

    retval
}

fn solve1(input: &Input) -> usize {
    let mut retval: HashSet<[i32; 2]> = HashSet::new();

    for (_id, positions) in input.antennas.iter() {
        let combinations = positions.iter().combinations(2);
        for combination in combinations {
            let antinodes = calculate_antinodes1(combination[0], combination[1]);
            for pos in antinodes {
                if pos[0] < 0
                    || pos[1] < 0
                    || pos[0] > input.height as i32 - 1
                    || pos[1] > input.width as i32 - 1
                {
                    continue;
                }
                retval.insert(pos);
            }
        }
    }

    retval.len()
}

fn solve2(input: &Input) -> usize {
    let mut retval: HashSet<[i32; 2]> = HashSet::new();

    for (_id, positions) in input.antennas.iter() {
        let combinations = positions.iter().combinations(2);
        for combination in combinations {
            let antinodes =
                calculate_antinodes2(combination[0], combination[1], input.width, input.height);
            for pos in antinodes {
                if !input.positions.contains_key(&pos) {
                    retval.insert(pos);
                }
            }
        }
    }

    // for (_id, positions) in input.antennas.iter() {
    //     let ttt = positions.iter().combinations(2).map(|combination| {
    //         calculate_antinodes2(combination[0], combination[1], input.width, input.height)
    //     });
    // }

    retval.len() + input.positions.len()
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");
    let input: Input = data.parse().unwrap();

    println!("{}", solve1(&input));
    println!("{}", solve2(&input));
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use crate::{calculate_antinodes1, solve1, solve2, Input};

    fn get_test_input() -> Input {
        Input::new(
            HashMap::from([
                ('A', vec![[5, 6], [8, 8], [9, 9]]),
                ('0', vec![[1, 8], [2, 5], [3, 7], [4, 4]]),
            ]),
            12,
            12,
        )
    }
    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_08_sample.txt");
        let input: Input = input_str.parse().unwrap();
        assert_eq!(
            input.antennas,
            HashMap::from([
                ('A', vec![[5, 6], [8, 8], [9, 9]]),
                ('0', vec![[1, 8], [2, 5], [3, 7], [4, 4]]),
            ])
        );
        assert_eq!(
            input.positions,
            HashMap::from([
                ([1, 8], '0'),
                ([5, 6], 'A'),
                ([8, 8], 'A'),
                ([4, 4], '0'),
                ([9, 9], 'A'),
                ([2, 5], '0'),
                ([3, 7], '0'),
            ])
        );
    }

    #[test]
    fn test_calculate_antinodes() {
        assert_eq!(calculate_antinodes1(&[3, 4], &[5, 5]), [[1, 3], [7, 6]]);
        assert_eq!(calculate_antinodes1(&[5, 5], &[3, 4]), [[7, 6], [1, 3]]);
        assert_eq!(calculate_antinodes1(&[4, 5], &[5, 4]), [[3, 6], [6, 3]]);
    }

    #[test]
    fn test_solve1() {
        let input = get_test_input();
        assert_eq!(solve1(&input), 14);
    }

    #[test]
    fn test_solve2() {
        let input = get_test_input();
        assert_eq!(solve2(&input), 34);
    }
}
