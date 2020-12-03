use std::io::{BufRead, BufReader};
use std::fs::File;
use std::env;

fn three_2020(data:&Vec<u32>) -> u32 {

    for val in data {
        let mut start = 2;
        for i in 1..data.len() {
            for j in start..data.len() {
                //println!("  {} : {} : {}", val, data[i], data[j]);
                if (val + data[i] + data[j]) == 2020 {
                    return val * data[i] * data[j]
                }
            }
            start += 1;
        }
    }

    panic!("No Match Found");
}

fn two_2020(data:&Vec<u32>) -> u32 {

    let mut start = 1;
    for val in data {
        for i in start..data.len() {
            //println!("  {} : {}", val, data[i]);
            if (val + data[i]) == 2020 {
                return val * data[i]
            }
        }
        start += 1;
    }
    panic!("No Match Found");
}


fn main() {

    let args: Vec<String> = env::args().collect();

    let reader = BufReader::new(File::open(&args[1]).expect("Cannot open file"));

    let mut data: Vec<u32> = vec![];

    for line in reader.lines() {
        data.push(line.unwrap().parse::<u32>().unwrap())
    }

    println!("Part 1: {}", two_2020(&data));
    println!("Part 2: {}", three_2020(&data));
}
