use clap::{command, Parser};
use regex::Regex;
#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_01.txt")]
    input: String,
}

fn solve1(data: &str) -> u32 {
    let re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();
    let mut retval: u32 = 0;
    for (_, [left, right]) in re.captures_iter(data).map(|c| c.extract()) {
        retval += left.parse::<u32>().unwrap() * right.parse::<u32>().unwrap();
    }
    retval
}

fn solve2(data: &str) -> u32 {
    let main_re = Regex::new(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))").unwrap();
    let mul_re = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)").unwrap();

    let mut enabled: bool = true;
    let mut retval: u32 = 0;

    for (_, [m1]) in main_re.captures_iter(data).map(|c| c.extract()) {
        match m1 {
            "do()" => {
                enabled = true;
            }
            "don't()" => {
                enabled = false;
            }
            _ if enabled => {
                let (_, [left, right]) = mul_re.captures(m1).unwrap().extract();
                retval += left.parse::<u32>().unwrap() * right.parse::<u32>().unwrap();
            }
            _ => {}
        }
    }
    retval
}
fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");
    println!("{}", solve1(data.as_str()));
    println!("{}", solve2(data.as_str()));
}
#[cfg(test)]
mod tests {
    use crate::{solve1, solve2};

    #[test]
    fn test_solve1() {
        let input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
        assert_eq!(solve1(input), 161);
    }

    #[test]
    fn test_solve2() {
        let input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
        assert_eq!(solve2(input), 48);
    }
}
