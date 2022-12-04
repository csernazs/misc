use std::fs::File;
use std::io::{BufRead, BufReader};

struct RangeSet {
    lower: u32,
    higher: u32,
}

impl RangeSet {
    fn issubset(&self, other: &RangeSet) -> bool {
        return self.lower >= other.lower && self.higher <= other.higher;
    }

    fn intersection(&self, other: &RangeSet) -> Option<RangeSet> {
        let new_lower: u32 = if other.lower > self.lower {
            other.lower
        } else {
            self.lower
        };

        let new_higher: u32 = if other.higher < self.higher {
            other.higher
        } else {
            self.higher
        };

        if new_lower <= new_higher {
            return Some(RangeSet {
                lower: new_lower,
                higher: new_higher,
            });
        } else {
            return None;
        }
    }
}

fn read_lines_from_file(path: &str) -> Vec<String> {
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines().map(|x| x.unwrap()).collect();
    return lines;
}

fn parse_pair(pair: &str) -> RangeSet {
    let splitted: Vec<&str> = pair.split("-").take(2).collect();
    let a: u32 = splitted[0].parse().unwrap();
    let b: u32 = splitted[1].parse().unwrap();
    return RangeSet {
        lower: a,
        higher: b,
    };
}

fn parse(lines: Vec<String>) -> Vec<(RangeSet, RangeSet)> {
    let mut retval: Vec<(RangeSet, RangeSet)> = vec![];

    for line in lines {
        let pairs: Vec<&str> = line.split(",").take(2).collect();
        let left = pairs[0];
        let right = pairs[1];
        let left_tuple = parse_pair(left);
        let right_tuple = parse_pair(right);

        retval.push((left_tuple, right_tuple));
    }

    return retval;
}

fn part_01(parsed: &Vec<(RangeSet, RangeSet)>) -> u32 {
    let mut cnt: u32 = 0;
    for pairs in parsed {
        let (left, right) = pairs;
        if left.issubset(&right) || right.issubset(&left) {
            cnt += 1;
        }
    }
    return cnt;
}

fn part_02(parsed: &Vec<(RangeSet, RangeSet)>) -> u32 {
    let mut cnt: u32 = 0;
    for pairs in parsed {
        let (left, right) = pairs;
        if left.intersection(&right).is_some() {
            cnt += 1;
        }
    }
    return cnt;
}

fn main() {
    let lines = read_lines_from_file("aoc_04.txt");
    let parsed = parse(lines);

    println!("{}", part_01(&parsed));
    println!("{}", part_02(&parsed));
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::*;

    // #[fixture]
    // fn input() -> Vec<String> {
    //     return vec![
    //         String::from("vJrwpWtwJgWrhcsFMMfFFhFp"),
    //         String::from("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"),
    //         String::from("PmmdzqPrVvPwwTWBwg"),
    //         String::from("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"),
    //         String::from("ttgJtRGJQctTZtZT"),
    //         String::from("CrZsJsPPZsGzwwsLwLmpwMDw"),
    //     ] as Vec<String>;
    // }

    #[rstest]
    fn test_resultset() {
        let rs = RangeSet {
            lower: 1,
            higher: 3,
        };
        assert!(rs.issubset(&RangeSet {
            lower: 1,
            higher: 10,
        }));
    }
}
