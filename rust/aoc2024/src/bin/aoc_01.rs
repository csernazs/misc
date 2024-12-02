use clap::Parser;
use std::collections::HashMap;
use std::hash::Hash;
use std::{num::ParseIntError, str::FromStr};

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_01.txt")]
    input: String,
}

#[derive(Debug, PartialEq)]
struct Input {
    left: Vec<u32>,
    right: Vec<u32>,
}

#[derive(Debug, PartialEq)]
enum ParseInputError {
    // Incorrect number of fields
    BadLen,
    // Wrapped error from parse::<u32>()
    ParseInt(ParseIntError),
}

impl FromStr for Input {
    type Err = ParseInputError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut left_vec: Vec<u32> = vec![];
        let mut right_vec: Vec<u32> = vec![];

        for line in s.lines() {
            let fields = line.split_whitespace().collect::<Vec<&str>>();
            if fields.len() != 2 {
                return Err(ParseInputError::BadLen);
            }
            left_vec.push(
                fields[0]
                    .to_string()
                    .parse::<u32>()
                    .map_err(ParseInputError::ParseInt)?,
            );
            right_vec.push(
                fields[1]
                    .to_string()
                    .parse::<u32>()
                    .map_err(ParseInputError::ParseInt)?,
            );
        }

        Ok(Input {
            left: left_vec,
            right: right_vec,
        })
    }
}

fn count<T>(input: Vec<T>) -> HashMap<T, u64>
where
    T: Eq,
    T: Hash,
{
    let mut retval: HashMap<T, u64> = HashMap::new();
    for item in input {
        retval.entry(item).and_modify(|x| *x += 1).or_insert(1);
    }
    retval
}

fn solve1(input: &Input) -> u32 {
    let mut left_sorted = input.left.clone();
    left_sorted.sort();

    let mut right_sorted = input.right.clone();
    right_sorted.sort();

    let zipped = left_sorted.into_iter().zip(right_sorted.into_iter());
    let mut retval: u32 = 0;
    for (left, right) in zipped {
        let diff = left.abs_diff(right);
        retval += diff;
    }
    retval
}

fn solve2(input: Input) -> u64 {
    let right_count = count(input.right.clone());

    input
        .left
        .into_iter()
        .map(|x| x as u64 * *right_count.get(&x).unwrap_or(&0))
        .sum()
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let input = data.parse::<Input>().unwrap();
    println!("{}", solve1(&input));
    println!("{}", solve2(input));
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    use crate::{count, solve1, solve2, Input};

    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_01_sample.txt");
        let input = input_str.to_string().parse::<Input>().unwrap();
        assert_eq!(
            input,
            Input {
                left: vec![3, 4, 2, 1, 3, 3],
                right: vec![4, 3, 5, 3, 9, 3],
            }
        );
    }

    #[test]
    fn test_solve1() {
        let input = Input {
            left: vec![3, 4, 2, 1, 3, 3],
            right: vec![4, 3, 5, 3, 9, 3],
        };
        assert_eq!(solve1(&input), 11);
    }

    #[test]
    fn test_solve2() {
        let input = Input {
            left: vec![3, 4, 2, 1, 3, 3],
            right: vec![4, 3, 5, 3, 9, 3],
        };
        assert_eq!(solve2(input), 31);
    }

    #[test]
    fn test_count() {
        assert_eq!(
            count(vec![1, 2, 3, 4, 1, 2, 3]),
            HashMap::from([(1, 2), (2, 2), (3, 2), (4, 1),])
        );
    }
}
