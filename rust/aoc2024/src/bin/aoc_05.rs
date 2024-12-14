use std::{collections::HashMap, str::FromStr};

use clap::{command, Parser};

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_01.txt")]
    input: String,
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Rule {
    left: i32,
    right: i32,
}

#[derive(Debug, PartialEq, Eq, Clone)]
struct Input {
    rules: Vec<Rule>,
    pages_list: Vec<Vec<i32>>,
    ordering: HashMap<i32, i32>,
}

impl Input {
    fn new(rules: Vec<Rule>, pages_list: Vec<Vec<i32>>) -> Self {
        let ordering = Self::get_ordering(&rules);
        Self {
            rules,
            pages_list,
            ordering,
        }
    }

    fn get_ordering(rules: &Vec<Rule>) -> HashMap<i32, i32> {
        let mut retval: HashMap<i32, i32> = HashMap::new();

        for rule in rules {
            *retval.entry(rule.left).or_insert(0) += 1;
        }
        retval
    }

    fn sort_pages(&self, input_vec: &[i32]) -> Vec<i32> {
        let mut foo: Vec<(i32, i32)> = input_vec
            .iter()
            .map(|&x| (x, *self.ordering.get(&x).unwrap_or(&-1)))
            .collect();

        foo.sort_by_key(|(_, right)| *right);

        foo.iter().rev().map(|(left, _)| *left).collect()
    }
}

#[derive(Debug, PartialEq, Eq, Copy, Clone)]
enum ParseError {
    BadNumOfFields,
}
impl FromStr for Rule {
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let fields: Vec<i32> = s.split('|').map(|x| x.parse().unwrap()).take(2).collect();
        if fields.len() != 2 {
            return Err(ParseError::BadNumOfFields);
        }

        Ok({
            Rule {
                left: fields[0],
                right: fields[1],
            }
        })
    }

    type Err = ParseError;
}

enum ParseState {
    Rules,
    Pages,
}

impl FromStr for Input {
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut state = ParseState::Rules;
        let mut rules = vec![];

        let mut pages_list = vec![];

        for line in s.lines() {
            match state {
                ParseState::Rules if line.is_empty() => state = ParseState::Pages,
                ParseState::Rules => rules.push(line.parse().unwrap()),
                ParseState::Pages => {
                    pages_list.push(line.split(',').map(|x| x.parse().unwrap()).collect())
                }
            }
        }
        Ok(Input::new(rules, pages_list))
    }

    type Err = ParseError;
}

fn solve1_for_pages(input: &Input, pages: &[i32]) -> bool {
    let new_pages = input.sort_pages(pages);
    // dbg!(pages);
    // dbg!(&new_pages);

    new_pages == pages
}

fn solve1(input: &Input) -> i32 {
    let mut retval = 0;

    for pages in &input.pages_list {
        if solve1_for_pages(input, pages) {
            let middle_item = *pages.get(pages.len() / 2).unwrap();
            retval += middle_item;
        }
    }
    retval
}
fn main() {
    let cli = Cli::parse();
    let data = std::fs::read_to_string(&cli.input).expect("Unable to open file");

    let input: Input = data.parse().unwrap();

    println!("{}", solve1(&input));
    // println!("{}", solve2(&input));
}

#[cfg(test)]
mod tests {
    use crate::{solve1, solve1_for_pages, Input, Rule};

    fn get_sample_input() -> Input {
        let rules = vec![
            Rule {
                left: 47,
                right: 53,
            },
            Rule {
                left: 97,
                right: 13,
            },
            Rule {
                left: 97,
                right: 61,
            },
            Rule {
                left: 97,
                right: 47,
            },
            Rule {
                left: 75,
                right: 29,
            },
            Rule {
                left: 61,
                right: 13,
            },
            Rule {
                left: 75,
                right: 53,
            },
            Rule {
                left: 29,
                right: 13,
            },
            Rule {
                left: 97,
                right: 29,
            },
            Rule {
                left: 53,
                right: 29,
            },
            Rule {
                left: 61,
                right: 53,
            },
            Rule {
                left: 97,
                right: 53,
            },
            Rule {
                left: 61,
                right: 29,
            },
            Rule {
                left: 47,
                right: 13,
            },
            Rule {
                left: 75,
                right: 47,
            },
            Rule {
                left: 97,
                right: 75,
            },
            Rule {
                left: 47,
                right: 61,
            },
            Rule {
                left: 75,
                right: 61,
            },
            Rule {
                left: 47,
                right: 29,
            },
            Rule {
                left: 75,
                right: 13,
            },
            Rule {
                left: 53,
                right: 13,
            },
        ];

        let pages_list = vec![
            vec![75, 47, 61, 53, 29],
            vec![97, 61, 53, 29, 13],
            vec![75, 29, 13],
            vec![75, 97, 47, 61, 53],
            vec![61, 13, 29],
            vec![97, 13, 75, 29, 47],
        ];

        Input::new(rules, pages_list)
    }
    #[test]
    fn test_parse() {
        let input_str = include_str!("aoc_05_sample.txt");

        let input: Input = input_str.parse().unwrap();

        assert_eq!(input, get_sample_input());
    }
    #[test]
    fn test_solve1_for_pages() {
        let input = get_sample_input();
        assert!(solve1_for_pages(&input, &[75, 47, 61, 53, 29]));
        assert!(solve1_for_pages(&input, &[97, 61, 53, 29, 13]));
        assert!(solve1_for_pages(&input, &[75, 29, 13]));
        assert!(!solve1_for_pages(&input, &[75, 97, 47, 61, 53]));
        assert!(!solve1_for_pages(&input, &[61, 13, 29]));
        assert!(!solve1_for_pages(&input, &[97, 13, 75, 29, 47]));
    }

    #[test]
    fn test_solve1() {
        let input = get_sample_input();
        assert_eq!(solve1(&input), 143);
    }
}
