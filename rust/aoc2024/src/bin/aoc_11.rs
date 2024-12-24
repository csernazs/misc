use clap::{command, Parser};
use std::hash::Hash;
use std::{collections::HashMap, num::ParseIntError, str::FromStr, time::Instant};

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_11.txt")]
    input: String,
}

#[derive(Debug, Clone)]
struct Counter<K>
where
    K: Eq + Hash,
{
    counts: HashMap<K, u64>,
}

impl<K> Counter<K>
where
    K: Eq + Hash,
{
    fn new() -> Self {
        Counter {
            counts: HashMap::new(),
        }
    }
    fn increase(&mut self, key: K) {
        self.increase_by(key, 1);
    }
    fn increase_by(&mut self, key: K, increment: u64) {
        self.counts
            .entry(key)
            .and_modify(|e| *e += increment)
            .or_insert(increment);
    }

    #[allow(dead_code)]
    fn update(&mut self, key: K, value: u64) {
        self.counts.insert(key, value);
    }

    #[allow(dead_code)]
    fn iter_keys(&self) -> impl Iterator<Item = &K> {
        self.counts
            .iter()
            .filter_map(|(key, value)| if *value > 1 { Some(key) } else { None })
    }
    fn sum(&self) -> u64 {
        self.counts.values().sum()
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
struct Input {
    numbers: Vec<u64>,
}

fn split_number(number: u64) -> Option<[u64; 2]> {
    let s = number.to_string();
    if s.is_empty() || s.len() % 2 != 0 {
        None
    } else {
        let (left, right) = s.split_at(s.len() / 2);
        Some([left.parse().unwrap(), right.parse().unwrap()])
    }
}
impl FromStr for Input {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let numbers: Result<Vec<u64>, ParseIntError> = s
            .split_whitespace()
            .filter(|x| !x.is_empty())
            .map(|x| x.parse::<u64>())
            .collect();

        Ok(Input { numbers: numbers? })
    }
}

fn blink(counter: &Counter<u64>) -> Counter<u64> {
    let mut new_counter: Counter<u64> = Counter::new();

    let count_zeroes = *counter.counts.get(&0).unwrap_or(&0);

    new_counter.increase_by(1, count_zeroes);

    let numbers: Vec<(&u64, &u64)> = counter
        .counts
        .iter()
        .filter(|(number, count)| **number > 0 && **count > 0)
        .collect();

    for (&number, &count) in numbers {
        match split_number(number) {
            Some([left, right]) => {
                new_counter.increase_by(left, count);
                new_counter.increase_by(right, count);
            }
            None => {
                new_counter.increase_by(number * 2024, count);
            }
        }
    }
    new_counter
}

fn solve(input: &Input, cnt: u32) -> u64 {
    let mut counter = Counter::new();
    input.numbers.iter().for_each(|n| counter.increase(*n));

    for _i in 0..cnt {
        counter = blink(&counter);
    }
    counter.sum()
}

fn solve2(input: &Input) -> u64 {
    solve(input, 75)
}

fn solve1(input: &Input) -> u64 {
    solve(input, 25)
}

fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let start = Instant::now();
    let input: Input = data.parse().unwrap();
    println!("{}", solve1(&input));
    println!("{}", solve2(&input));
    let duration = start.elapsed();
    println!("Elapsed time: {} ms", duration.as_millis());
}

#[cfg(test)]
mod tests {
    use crate::{solve1, solve2, split_number, Input};

    fn get_example_input() -> Input {
        Input {
            numbers: vec![0, 1, 10, 99, 999],
        }
    }
    #[test]
    fn test_parse() {
        let example = "0 1 10 99 999";
        let input: Input = example.parse().unwrap();
        assert_eq!(input, get_example_input());
    }
    #[test]
    fn test_split() {
        assert_eq!(split_number(1234).unwrap(), [12, 34]);
        assert_eq!(split_number(12345), None);
        assert_eq!(split_number(9876).unwrap(), [98, 76]);
    }

    #[test]
    fn test_solve1() {
        let input = "125 17".parse().unwrap();
        assert_eq!(solve1(&input), 55312);
    }

    #[test]
    fn test_solve2() {
        let input = "125 17".parse().unwrap();
        assert_eq!(solve2(&input), 65601038650482);
    }
}
