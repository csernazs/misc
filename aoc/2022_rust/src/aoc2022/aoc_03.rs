use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn part01(lines: Vec<String>) -> usize {
    let mut retval: usize = 0;
    let letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXZ";

    for line in lines {
        let left = line.get(0..line.len() / 2).unwrap();
        let right = line.get(line.len() / 2..).unwrap();
        let left_set: HashSet<char> = left.chars().into_iter().collect();
        let right_set: HashSet<char> = right.chars().into_iter().collect();

        let mut common = left_set.intersection(&right_set).clone();

        let item = common.nth(0).unwrap().clone();
        retval += letters.find(item).unwrap() + 1;
    }
    return retval;
}

fn read_lines_from_file(path: &str) -> Vec<String> {
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines().map(|x| x.unwrap()).collect();
    return lines;
}
fn main() {
    let lines = read_lines_from_file("aoc_03.txt");
    println!("{}", part01(lines));
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::*;

    #[fixture]
    fn input() -> Vec<String> {
        return vec![
            String::from("vJrwpWtwJgWrhcsFMMfFFhFp"),
            String::from("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"),
            String::from("PmmdzqPrVvPwwTWBwg"),
            String::from("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"),
            String::from("ttgJtRGJQctTZtZT"),
            String::from("CrZsJsPPZsGzwwsLwLmpwMDw"),
        ] as Vec<String>;
    }

    #[rstest]
    fn test_first(input: Vec<String>) {
        let result = part01(input);

        assert_eq!(result, 157);
    }
}
