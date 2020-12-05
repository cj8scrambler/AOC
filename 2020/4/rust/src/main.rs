use std::io::{BufRead, BufReader};
use std::fs::File;
use std::env;
use std::collections::HashMap;
use regex::Regex;

fn validate_part1(passport:&HashMap<&String, &String>) -> bool {
    println!("Validate Passport");
    return true;
}

    //let re = Regex::new(r"(?P<min>\d+)-(?P<max>\d+)\s*(?P<char>\w):\s*(?P<pass>\w+$)").unwrap();

fn main() {

    let args: Vec<String> = env::args().collect();
    let reader = BufReader::new(File::open(&args[1]).expect("Cannot open file"));

    // Parse (blank line is new record)
    // ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    // byr:1937 iyr:2017 cid:147 hgt:183cm

    let mut passport = HashMap::new();
    passport.insert("".to_string(), "".to_string());

    let mut valid1 = 0;
    for line in reader.lines() {
        let line = line.unwrap();
        println!("{}", line);
        if line == "" {
//            valid1 += validate_part1(&passport) as u32;
              for mut key in passport.keys() {
                  passport.remove(key);
              }
        } else {
            let linedata = line.split_whitespace()
                               .map(|word| word.split(':'))
                               .map(|mut token| (token.next().unwrap().into(), token.next().unwrap().into()))
                               .collect::<HashMap<String, String>>();
            passport.extend(linedata);
            println!("Updated passport to {:?}", passport);
        }
    }
    //println!("Part 1 valid passwds: {}", valid1);
    //println!("Part 2 valid passwds: {}", valid2);
}
