use std::{num::ParseIntError, str::FromStr};

use clap::Parser;

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_01.txt")]
    input: String,
}

#[derive(Debug, PartialEq, Clone)]
struct Report {
    levels: Vec<u32>,
}

impl Report {
    fn is_safe_dec(self: &Self) -> bool {
        let mut old: u32 = self.levels[0];

        for &current in &self.levels[1..] {
            let diff: i64 = old as i64 - current as i64;

            if diff < 1 || diff > 3 {
                return false;
            }
            old = current;
        }
        true
    }

    fn is_safe_inc(self: &Self) -> bool {
        let mut old: u32 = self.levels[0];

        for &current in &self.levels[1..] {
            let diff: i64 = current as i64 - old as i64;
            dbg!(diff);
            if diff < 1 || diff > 3 {
                return false;
            }
            old = current;
        }
        true
    }

    fn is_safe_1(self: &Self) -> bool {
        self.is_safe_inc() || self.is_safe_dec()
    }

    fn clone_with_removed_index(self: &Self, idx: usize) -> Report {
        let mut new_levels = self.levels.clone();
        new_levels.remove(idx);
        Report { levels: new_levels }
    }

    fn is_safe_2(&self) -> bool {
        if self.is_safe_1() {
            return true;
        }

        for idx in 0..self.levels.len() {
            let new_report = self.clone_with_removed_index(idx);
            if new_report.is_safe_1() {
                return true;
            }
        }
        false
    }
}

impl FromStr for Report {
    type Err = ParseIntError;
    fn from_str(line: &str) -> Result<Self, Self::Err> {
        let results: Result<Vec<u32>, _> = line.split_whitespace().map(|x| x.parse()).collect();

        match results {
            Ok(levels) => Ok(Report { levels }),
            Err(e) => Err(e),
        }
    }
}

#[derive(Debug, PartialEq)]
struct Input {
    reports: Vec<Report>,
}

impl FromStr for Input {
    type Err = ParseIntError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let results: Result<Vec<Report>, _> = s.lines().map(|x| x.parse()).collect();
        match results {
            Ok(reports) => Ok(Input { reports }),
            Err(e) => Err(e),
        }
    }
}

fn solve1(input: &Input) -> usize {
    input.reports.iter().filter(|x| x.is_safe_1()).count()
}

fn solve2(input: &Input) -> usize {
    input.reports.iter().filter(|x| x.is_safe_2()).count()
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let input = data.parse::<Input>().unwrap();

    println!("{}", solve1(&input));
    println!("{}", solve2(&input));
}

mod tests {
    use crate::{solve1, solve2, Input, Report};

    fn get_input() -> Input {
        Input {
            reports: vec![
                Report {
                    levels: vec![7, 6, 4, 2, 1],
                },
                Report {
                    levels: vec![1, 2, 7, 8, 9],
                },
                Report {
                    levels: vec![9, 7, 6, 2, 1],
                },
                Report {
                    levels: vec![1, 3, 2, 4, 5],
                },
                Report {
                    levels: vec![8, 6, 4, 4, 1],
                },
                Report {
                    levels: vec![1, 3, 6, 7, 9],
                },
            ],
        }
    }
    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_02_sample.txt");
        let input = input_str.to_string().parse::<Input>().unwrap();
        assert_eq!(input, get_input());
    }

    #[test]
    fn test_solve1() {
        assert_eq!(solve1(&get_input()), 2);
    }

    #[test]
    fn test_solve2() {
        assert_eq!(solve2(&get_input()), 4);
    }

    #[test]
    fn test_solve2_case1() {
        assert!(Report {
            levels: vec![1, 4, 2, 3, 6]
        }
        .is_safe_2());
    }
}
