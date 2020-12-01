use std::{fs::File, io::Read, path::Path};

fn read_file(path: &Path) -> Vec<i64> {
    let mut file = File::open(&path).expect("Unable to open file");
    let mut s = String::new();
    file.read_to_string(&mut s).expect("Unable to read file");

    return s
        .lines()
        .map(|x| x.parse::<i64>().expect("Unable to parse int"))
        .collect();
}

fn main() {
    let numbers = read_file(Path::new("aoc_01.txt"));
    for i in 0..numbers.len() {
        for j in i + 1..numbers.len() {
            if numbers[i] + numbers[j] == 2020 {
                println!("{}", numbers[i] * numbers[j]);
                break;
            }
        }
    }
    for i in 0..numbers.len() {
        for j in i + 1..numbers.len() {
            for k in j + 1..numbers.len() {
                if numbers[i] + numbers[j] + numbers[k] == 2020 {
                    println!("{}", numbers[i] * numbers[j] * numbers[k]);
                    break;
                }
            }
        }
    }
}
