#!/usr/bin/python

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
  
def showme(data):
    for line in data:
        logging.info("  {0}".format(line))

def part1(data):
    valid = 0
    for record in data:
        logging.debug("record: {}".format(record))
        valid += validate1(record)
    return valid

def validate1(record):
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for r in required:
        if not record.has_key(r):
            logging.debug("  record is missing %s", r);
            return False
    logging.debug("  record is valid");
    return True

def part2(data):
    valid = 0
    for record in data:
        logging.debug("record: {}".format(record))
        valid += validate2(record)
    return valid

def validate2(record):
    validator = {
            'byr': validate_byr,
            'iyr': validate_iyr,
            'eyr': validate_eyr,
            'hgt': validate_hgt,
            'hcl': validate_hcl,
            'ecl': validate_ecl,
            'pid': validate_pid
    }

    for v in validator.keys():
        if not record.has_key(v):
            logging.debug("  record is invalid (missing %s)", v);
            return False
        if not validator[v](record[v]):
            logging.debug("  record is invalid (fails %s test)", v);
            return False
    logging.debug("  record is valid");
    return True

def validate_byr(d):
    #four digits; at least 1920 and at most 2002.
    if int(d) >= 1920 and int(d) <= 2002:
        logging.debug("    byr valid: %s", d);
        return True;
    logging.debug("    byr invalid: %s", d);
    return False;

def validate_iyr(d):
    #four digits; at least 2010 and at most 2020.
    if int(d) >= 2010 and int(d) <= 2020:
        logging.debug("    iyr valid: %s", d);
        return True;
    logging.debug("    iyr invalid: %s", d);
    return False;

def validate_eyr(d):
    # four digits; at least 2020 and at most 2030
    if int(d) >= 2020 and int(d) <= 2030:
        logging.debug("    eyr valid: %s", d);
        return True;
    logging.debug("    eyr invalid: %s", d);
    return False;

def validate_hgt(d):
    #a number followed by either cm or in:
    #  If cm, the number must be at least 150 and at most 193.
    #  If in, the number must be at least 59 and at most 76.
    pattern = re.compile(r"(?P<val>\d+)(?P<unit>\w+)")
    data = pattern.match(d).groupdict()

    if (data['unit'] == 'cm'):
        if int(data['val']) >= 150 and int(data['val']) <= 193:
            logging.debug("    hgt valid: %s", d);
            return True;
        logging.debug("    hgt invalid: %s", d);
        return False;
    if (data['unit'] == 'in'):
        if int(data['val']) >= 59 and int(data['val']) <= 76:
            logging.debug("    hgt valid: %s", d);
            return True;
        logging.debug("    hgt invalid: %s", d);
        return False;

    logging.debug("    hgt bad unit: %s", data['unit']);
    return False;

def validate_hcl(d):
    pattern = re.compile(r"^#[0-9a-f]{6}$")
    if (pattern.match(d) is None):
        logging.debug("    hcl invalid: %s", d);
        return False
    logging.debug("    hcl valid: %s", d);
    return True;

def validate_ecl(d):
    # exactly one of: amb blu brn gry grn hzl oth.
    required = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    if d in required:
        logging.debug("    ecl valid: %s", d);
        return True;
    logging.debug("    ecl invalid: %s", d);
    return False;

def validate_pid(d):
    #a nine-digit number, including leading zeroes.
    pattern = re.compile(r"^[0-9]{9}$")
    if (pattern.match(d) is None):
        logging.debug("    pid invalid: %s", d);
        return False
    logging.debug("    pid valid: %s", d);
    return True;

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    data.append({})
    for line in fileinput.input():
        #logging.debug("line: '%s'" % (line))
        if line == "\n":
            # Make a new record
            data.append({})
        else:
            for word in line.split():
                t = word.split(':')
                data[-1][t[0]] = t[1]

        #logging.debug(" record: {0}".format(data[-1]))
    #showme(data);
    print("Part 1 valid passports: %d" % (part1(data)))
    print("Part 2 valid passports: %d" % (part2(data)))
