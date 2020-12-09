use core::panic;
use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
};

#[derive(Debug, Clone, Copy)]
enum Instruction {
    NOP(i64),
    ACC(i64),
    JMP(i64),
}

#[derive(Debug)]
struct ProgramResult {
    acc: i64,
    has_loop: bool,
}

fn parse_file(path: String) -> Vec<Instruction> {
    let file = File::open(path).expect("Unable to open file");
    let reader = BufReader::new(file);
    let mut retval: Vec<Instruction> = Vec::new();

    for line_result in reader.lines() {
        let line = line_result.expect("Unable to read line");
        let fields: Vec<&str> = line.split(" ").collect();
        let arg: i64 = fields[1]
            .trim_start_matches("+")
            .parse()
            .expect(&format!("Error: {}", fields[1].trim_start_matches("+")));

        let instr = match fields[0] {
            "acc" => Instruction::ACC(arg),
            "jmp" => Instruction::JMP(arg),
            "nop" => Instruction::NOP(arg),
            _ => panic!("Invalid operation: {}", fields[0]),
        };

        retval.push(instr);
    }

    return retval;
}

fn run_program(program: &Vec<Instruction>) -> ProgramResult {
    let mut acc: i64 = 0;
    let mut ip: i64 = 0;
    let mut seen: HashSet<i64> = HashSet::new();

    loop {
        if seen.contains(&ip) {
            return ProgramResult {
                acc,
                has_loop: true,
            };
        }
        seen.insert(ip);
        if ip as usize > program.len() - 1 {
            return ProgramResult {
                acc,
                has_loop: false,
            };
        }
        let ref instr = program[ip as usize];

        match instr {
            Instruction::NOP(_) => {
                ip += 1;
            }
            Instruction::ACC(arg) => {
                acc += arg;
                ip += 1;
            }
            Instruction::JMP(arg) => {
                ip += arg;
            }
        }
    }
}
fn solve_1(program: &Vec<Instruction>) -> i64 {
    return run_program(&program).acc;
}

fn solve_2(program: &Vec<Instruction>) -> Option<i64> {
    let mut my_program = program.to_vec();

    for idx in 0..my_program.len() {
        let ref instr = my_program[idx];
        my_program[idx] = match instr {
            Instruction::JMP(arg) => Instruction::NOP(*arg),
            Instruction::NOP(arg) => Instruction::JMP(*arg),
            Instruction::ACC(_) => continue,
        };
        let result = run_program(&my_program);
        if !result.has_loop {
            return Some(result.acc);
        }
        my_program[idx] = match my_program[idx] {
            Instruction::JMP(arg) => Instruction::NOP(arg),
            Instruction::NOP(arg) => Instruction::JMP(arg),
            x => x,
        };
    }

    return None;
}

fn main() {
    let program = parse_file("../aoc_08.txt".to_string());
    println!("solve_1: {}", solve_1(&program));
    println!("solve_2: {}", solve_2(&program).unwrap());
}
