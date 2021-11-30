#!/usr/bin/python

import logging
import sys
import fileinput
import time
import math
import re
from itertools import combinations 
from itertools import permutations 
  
def apply(data, ruleset, rulenum):

    logging.debug("  apply({}, {})".format(data, rulenum))
    if (len(data) == 0):
        logging.debug("    apply() at the end; return false")
        return False;
    if ('alpha' in ruleset[rulenum]):
        if data[0] == ruleset[rulenum]['alpha']:
            logging.debug("    apply() on alpha: return True and pop(0)")
            data.pop(0)
            return True
        else:
            logging.debug("    apply() on alpha: no match; return False")
            return False
    for eachnext in ruleset[rulenum]['next']:
        allmatch = True
        logging.debug("    apply() rule {} part: {}".format(rulenum, eachnext))
        for nextrule in eachnext:
            if not apply(data, ruleset, nextrule):
                logging.debug("    apply() rule {} part: {} failed; return false".format(rulenum, eachnext))
                allmatch = False
                break;
        if allmatch:
            logging.debug("    apply() rule {} part: {} passed all parts; return True".format(rulenum, eachnext))
            return True

    logging.debug("    apply({}) failed".format(rulenum))
    return False

def validate(word, ruleset):

    logstr="validate({})".format(word)
    logging.debug(logstr)
    result = apply(word, ruleset, 0)
    if (len(word)):
        logging.debug("extra chars found")
        result = False
    logstr+=" returned {}".format(result)
    logging.info(logstr)
    return result

def part1(data, ruleset):

    for word in data:
        validate(word, ruleset)

    return 0

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    pat = re.compile(r"^([\d]+): (.*)$")

    data = []
    ruleset = {}

    ondata = False
    for line in fileinput.input():
        if (len(line) <= 1):
            ondata = True
            continue
        if ondata:
            data.append(list(line.rstrip()))

        match = pat.match(line)
        if match:
            rulenum = int(match.group(1))
            rule = match.group(2).strip('"').split()
            if rule[0].isalpha():
                ruleset[rulenum] = {'alpha': rule[0]}
            else:
                ruleset[rulenum] = {'next': []}
                for each in match.group(2).split('|'):
                    rulerange = [int(i) for i in each.lstrip().rstrip().split()]
                    ruleset[rulenum]['next'].append(rulerange)

    logging.debug("Rule set: {}".format(ruleset))
    logging.debug("Data: {}".format(data))
    result = part1(data, ruleset)
    print("Part1: %d" % result)
    #result = part2(data)
    #print("Part2 {0}".format(timestamp))
