use std::{fmt::Display, str::FromStr};

use clap::{command, Parser};
use itertools::Itertools;

#[derive(Parser, Debug, Clone)]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, default_value = "aoc_07.txt")]
    input: String,
}

#[derive(Debug, Clone, PartialEq)]

enum BlockType {
    Free,
    Taken,
}
#[derive(Debug, Clone, PartialEq)]
enum Block {
    Free { length: i32 },
    Taken { length: i32, value: i32 },
}

impl Block {
    fn get_length(&self) -> i32 {
        match self {
            Block::Free { length } => *length,
            Block::Taken { length, value: _ } => *length,
        }
    }

    fn get_value(&self) -> i32 {
        match self {
            Block::Free { length: _ } => -1,
            Block::Taken { length: _, value } => *value,
        }
    }
}
#[derive(Debug, Clone, PartialEq)]
struct Input {
    map: Vec<Block>,
}

impl FromStr for Input {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut map: Vec<Block> = vec![];

        let mut iterator = [BlockType::Taken, BlockType::Free].into_iter().cycle();
        for (value, length_char) in s.chars().enumerate() {
            let length = match length_char.to_digit(10) {
                Some(length) => length as i32,
                None => continue,
            };

            let blocktype = iterator.next().unwrap();

            let block_option = match blocktype {
                BlockType::Free if length > 0 => Some(Block::Free { length }),
                BlockType::Free => None,
                BlockType::Taken => Some(Block::Taken {
                    length,
                    value: (value / 2) as i32,
                }),
            };
            if let Some(block) = block_option {
                map.push(block);
            }
        }
        Ok(Input { map })
    }
}

impl Display for Block {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let as_str = match self {
            Block::Free { length } => ".".repeat(*length as usize),
            Block::Taken { length, value } => value.to_string().repeat(*length as usize),
        };
        write!(f, "{}", as_str)?;
        Ok(())
    }
}
impl Display for Input {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for block in self.map.iter() {
            write!(f, "{}", block)?;
        }
        Ok(())
    }
}

impl Input {
    fn inflate(&self) -> Vec<i32> {
        self.map
            .iter()
            .flat_map(|block| match block {
                Block::Free { length } => vec![-1; *length as usize].into_iter(),
                Block::Taken { length, value } => vec![*value; *length as usize].into_iter(),
            })
            .collect()
    }

    fn iter_taken_from_right(&self) -> impl Iterator<Item = (usize, &Block)> {
        self.map
            .iter()
            .enumerate()
            .rev()
            .filter_map(|(idx, block)| match *block {
                Block::Free { length: _ } => None,
                Block::Taken {
                    length: _,
                    value: _,
                } => Some((idx, block)),
            })
    }
}

#[allow(dead_code)]
fn format_inflated(inflated: &[i32]) -> String {
    inflated
        .iter()
        .map(|&num| {
            if num == -1 {
                ".".to_string()
            } else {
                num.to_string()
            }
        })
        .join("")
}

fn move_block(map: &mut [i32], value: i32, target: usize) {
    let found: Vec<(usize, usize)> = map
        .iter()
        .enumerate()
        .filter_map(|(idx, &x)| if x == value { Some(idx) } else { None })
        .zip(target..)
        .collect();

    for (src_idx, target_idx) in found {
        if target_idx < src_idx {
            map.swap(src_idx, target_idx);
        }
    }
}

fn defrag2(input: &Input) -> Vec<i32> {
    let mut inflated = input.inflate();

    let taken_iterator = input.iter_taken_from_right();

    let mut free_cnt = 0;

    for (_taken_idx, taken_block) in taken_iterator {
        for idx in 0..inflated.len() {
            let item = inflated[idx];
            if item == -1 {
                free_cnt += 1;
                if free_cnt == taken_block.get_length() {
                    move_block(
                        &mut inflated,
                        taken_block.get_value(),
                        idx - free_cnt as usize + 1,
                    );
                    break;
                }
            } else {
                free_cnt = 0;
            }
        }
    }

    inflated
}

fn defrag1(map: &[i32]) -> Vec<i32> {
    let mut new_map: Vec<i32> = vec![];
    let mut reversed = map.iter();

    let taken_count = map.iter().filter(|x| **x > -1).count();

    for &value in map.iter() {
        if new_map.len() == taken_count {
            break;
        }

        if value > -1 {
            new_map.push(value);
            continue;
        };

        let taken_value = reversed.rfind(|value| **value > -1).unwrap();

        new_map.push(*taken_value);
    }
    new_map
}

fn get_checksum(map: &[i32]) -> usize {
    map.iter()
        .enumerate()
        .filter_map(|(idx, &value)| {
            if value > 0 {
                Some(idx * value as usize)
            } else {
                None
            }
        })
        .sum()
}
fn solve1(input: &Input) -> usize {
    println!("{}", input.map.len());

    let inflated = input.inflate();

    let defragged = defrag1(&inflated);

    get_checksum(&defragged)
}

fn solve2(input: &Input) -> usize {
    let defragged = defrag2(input);
    get_checksum(&defragged)
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

    use crate::defrag1;
    use crate::defrag2;
    use crate::format_inflated;
    use crate::solve1;
    use crate::Block;
    use crate::Block::*;
    use crate::Input;

    fn get_sample_input() -> Input {
        Input {
            map: vec![
                Taken {
                    length: 2,
                    value: 0,
                },
                Free { length: 3 },
                Taken {
                    length: 3,
                    value: 1,
                },
                Free { length: 3 },
                Taken {
                    length: 1,
                    value: 2,
                },
                Free { length: 3 },
                Taken {
                    length: 3,
                    value: 3,
                },
                Free { length: 1 },
                Taken {
                    length: 2,
                    value: 4,
                },
                Free { length: 1 },
                Taken {
                    length: 4,
                    value: 5,
                },
                Free { length: 1 },
                Taken {
                    length: 4,
                    value: 6,
                },
                Free { length: 1 },
                Taken {
                    length: 3,
                    value: 7,
                },
                Free { length: 1 },
                Taken {
                    length: 4,
                    value: 8,
                },
                Taken {
                    length: 2,
                    value: 9,
                },
            ],
        }
    }
    #[test]
    fn test_parse() {
        let input_s = "2333133121414131402";
        let input: Input = input_s.parse().unwrap();

        assert_eq!(input, get_sample_input());
    }

    #[test]
    fn test_parse2() {
        let input_s = "00000010";
        let input: Input = input_s.parse().unwrap();

        assert_eq!(
            input,
            Input {
                map: vec![
                    Taken {
                        length: 0,
                        value: 0
                    },
                    Taken {
                        length: 0,
                        value: 1
                    },
                    Taken {
                        length: 0,
                        value: 2
                    },
                    Taken {
                        length: 1,
                        value: 3
                    }
                ]
            }
        );

        assert_eq!(input.inflate(), vec![3]);
    }

    #[test]
    fn test_inflate() {
        let input = get_sample_input();
        let inflated = input.inflate();
        assert_eq!(
            inflated,
            vec![
                0, 0, -1, -1, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5,
                5, 5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, 9, 9
            ]
        );
    }

    #[test]
    fn test_inflate2() {
        let input: Input = "1211112".parse().unwrap();
        let inflated = input.inflate();
        assert_eq!(inflated, vec![0, -1, -1, 1, -1, 2, -1, 3, 3]);
        let defragged = defrag1(&inflated);

        assert_eq!(defragged, vec![0, 3, 3, 1, 2]);
    }

    #[test]
    fn test_defrag() {
        let inflated: Vec<i32> = vec![
            0, 0, -1, -1, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5,
            5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, 9, 9,
        ];
        assert_eq!(
            defrag1(&inflated),
            vec![
                0, 0, 9, 9, 8, 1, 1, 1, 8, 8, 8, 2, 7, 7, 7, 3, 3, 3, 6, 4, 4, 6, 5, 5, 5, 5, 6, 6,
            ]
        );
    }
    #[test]
    fn test_solve1() {
        let input = get_sample_input();
        assert_eq!(solve1(&input), 1928);
    }
    #[test]
    fn test_format_block() {
        let free = Block::Free { length: 10 };
        assert_eq!(format!("{}", free), "..........");

        let taken = Block::Taken {
            length: 5,
            value: 3,
        };
        assert_eq!(format!("{}", taken), "33333");

        let input = Input {
            map: vec![taken, free],
        };
        assert_eq!(format!("{}", input), "33333..........");
    }
    #[test]
    fn test_format_inflated() {
        let inflated: Vec<i32> = vec![
            0, 0, -1, -1, -1, 1, 1, 1, -1, -1, -1, 2, -1, -1, -1, 3, 3, 3, -1, 4, 4, -1, 5, 5, 5,
            5, -1, 6, 6, 6, 6, -1, 7, 7, 7, -1, 8, 8, 8, 8, 9, 9,
        ];
        assert_eq!(
            format_inflated(&inflated),
            "00...111...2...333.44.5555.6666.777.888899"
        );
    }

    #[test]
    fn test_defrag2() {
        let input = get_sample_input();
        let defragged = defrag2(&input);
        assert_eq!(
            format_inflated(&defragged),
            "00992111777.44.333....5555.6666.....8888.." // "0099.111...2...333.44.5555.6666.777.8888.."
        );
    }
}
