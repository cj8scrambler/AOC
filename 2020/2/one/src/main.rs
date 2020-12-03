use std::io::{BufRead, BufReader};
use std::fs::File;
use std::env;
use regex::Regex;

fn validate_part1(min:u8, max:u8, value:char, pass:&str) -> bool {
    //println!("min: {}  max: {}  char: {}  pass: {}", min, max, value, pass);
    let mut count=0;
    for each in pass.chars() {
        count += (each == value) as u8;
    }
    //println!("count: {}", count);
    return (count >= min) && (count <= max);
}

fn validate_part2(first:u8, second:u8, value:char, pass:&str) -> bool {
    //println!("first: {}  second: {}  char: {}  pass: {}", first, second, value, pass);
    
    // return: (pass[first-1] == value) XOR (pass[second-1] == value)
    return (pass.chars().nth((first-1).into()).unwrap() == value) !=
           (pass.chars().nth((second-1).into()).unwrap() == value);
}


fn main() {

    let args: Vec<String> = env::args().collect();

    let reader = BufReader::new(File::open(&args[1]).expect("Cannot open file"));

    // Parse:
    // 1-3 a: abcde
    let re = Regex::new(r"(?P<min>\d+)-(?P<max>\d+)\s*(?P<char>\w):\s*(?P<pass>\w+$)").unwrap();

    let mut valid1:u32 = 0;
    let mut valid2:u32 = 0;
    for line in reader.lines() {
        //println!("{:?}", line);
        for cap in re.captures_iter(&line.unwrap()) {
            valid1 += validate_part1(cap["min"].parse().unwrap(),
                                     cap["max"].parse().unwrap(),
                                     cap["char"].parse().unwrap(),
                                     &cap["pass"]) as u32;
            valid2 += validate_part2(cap["min"].parse().unwrap(),
                                     cap["max"].parse().unwrap(),
                                     cap["char"].parse().unwrap(),
                                     &cap["pass"]) as u32;
        }
    }
    println!("Part 1 valid passwds: {}", valid1);
    println!("Part 2 valid passwds: {}", valid2);
}
