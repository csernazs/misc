use std::{fmt::Debug, iter::repeat};

use clap::{command, Parser};
use itertools::Itertools;
use nom::{
    bytes::complete::tag,
    character::complete::{digit1, space1},
    combinator::map_res,
    multi::separated_list1,
    sequence::separated_pair,
    IResult,
};
use nom_supreme::{error::ErrorTree, final_parser::final_parser};

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_07.txt")]
    input: String,
}

fn number(input: &str) -> IResult<&str, u64, ErrorTree<&str>> {
    map_res(digit1, str::parse::<u64>)(input)
}

fn list_of_ints(input: &str) -> IResult<&str, Vec<u64>, ErrorTree<&str>> {
    separated_list1(space1, number)(input)
}

fn parse_line(input: &str) -> Result<(u64, Vec<u64>), ErrorTree<&str>> {
    final_parser(separated_pair(number, tag(": "), list_of_ints))(input)
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum Op {
    Add,
    Mul,
    Concat,
}

fn solve_line(test_value: u64, numbers: &[u64], combinations: &[Op]) -> bool {
    let product = repeat(combinations)
        .take(numbers.len() - 1)
        .multi_cartesian_product();

    // println!("New line");
    for combination in product {
        // dbg!(&combination);
        let mut combination_iter = combination.iter();

        let tmp_value = numbers
            .iter()
            .copied()
            .reduce(|a, b| {
                let op = combination_iter.next().unwrap();
                match op {
                    Op::Add => a.checked_add(b).unwrap(),
                    Op::Mul => a.checked_mul(b).unwrap(),
                    Op::Concat => format!("{}{}", a, b).parse().unwrap(),
                }
            })
            .unwrap();
        if tmp_value == test_value {
            return true;
        }
    }

    false
}

fn solve1(data: &Vec<&str>) -> u64 {
    let mut retval: u64 = 0;
    for line in data {
        // println!("{}", line);
        let (test_value, numbers) = parse_line(line).unwrap();

        if solve_line(test_value, &numbers, &[Op::Add, Op::Mul]) {
            retval = retval.checked_add(test_value).unwrap();
        }
    }
    retval
}

fn solve2(data: &Vec<&str>) -> u64 {
    let mut retval: u64 = 0;
    for line in data {
        // println!("{}", line);
        let (test_value, numbers) = parse_line(line).unwrap();

        if solve_line(test_value, &numbers, &[Op::Add, Op::Mul, Op::Concat]) {
            retval = retval.checked_add(test_value).unwrap();
        }
    }
    retval
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let lines = data.lines().collect();
    println!("{}", solve1(&lines));
    println!("{}", solve2(&lines));
}

#[cfg(test)]
mod tests {
    use crate::{parse_line, solve1, solve2};

    #[test]
    fn test_parse_line() {
        let data = parse_line("267884545235: 9 8 3 930 6 6 4 98 3 7 9 7").unwrap();
        assert_eq!(
            data,
            (267884545235, vec![9, 8, 3, 930, 6, 6, 4, 98, 3, 7, 9, 7])
        )
    }

    #[test]
    fn test_solve1() {
        let input_str = include_str!("aoc_07_sample.txt");
        assert_eq!(solve1(&input_str.lines().collect()), 3749);
    }

    #[test]
    fn test_solve2() {
        let input_str = include_str!("aoc_07_sample.txt");
        assert_eq!(solve2(&input_str.lines().collect()), 11387);
    }
}
