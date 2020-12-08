use core::panic;
use std::convert::TryFrom;
use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
};

#[derive(Debug, Clone, Copy)]
enum Operation {
    NOP,
    ACC,
    JMP,
}
#[derive(Clone)]
struct Instruction {
    op: Operation,
    arg: i16,
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

        let op = match fields[0] {
            "acc" => Operation::ACC,
            "jmp" => Operation::JMP,
            "nop" => Operation::NOP,
            _ => panic!("Invalid operation: {}", fields[0]),
        };
        let arg = fields[1]
            .trim_start_matches("+")
            .parse()
            .expect(&format!("Error: {}", fields[1].trim_start_matches("+")));

        retval.push(Instruction { op, arg });
    }

    return retval;
}

fn run_program(program: &Vec<Instruction>) -> ProgramResult {
    let mut acc: i64 = 0;
    let mut ip: usize = 0;
    let mut seen: HashSet<usize> = HashSet::new();

    loop {
        if seen.contains(&ip) {
            return ProgramResult {
                acc,
                has_loop: true,
            };
        }
        seen.insert(ip);
        if ip > program.len() - 1 {
            return ProgramResult {
                acc,
                has_loop: false,
            };
        }
        let ref instr = program[ip];
        // println!("ip: {}, op: {:?}, arg: {}", ip, instr.op, instr.arg);

        match instr.op {
            Operation::NOP => {
                ip += 1;
            }
            Operation::ACC => {
                acc += i64::from(instr.arg);
                ip += 1;
            }
            Operation::JMP => {
                let new_ip = i64::try_from(ip).unwrap() + i64::from(instr.arg);
                ip = usize::try_from(new_ip).unwrap();
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
        my_program[idx].op = match instr.op {
            Operation::JMP => Operation::NOP,
            Operation::NOP => Operation::JMP,
            Operation::ACC => continue,
        };
        let result = run_program(&my_program);
        if !result.has_loop {
            return Some(result.acc);
        }
        my_program[idx].op = match my_program[idx].op {
            Operation::JMP => Operation::NOP,
            Operation::NOP => Operation::JMP,
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
