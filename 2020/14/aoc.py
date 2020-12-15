#!/usr/bin/python

import logging
import sys
import fileinput
import time
import math
import re
from itertools import combinations,permutations

def str_or(val, mask):

    result = ""
    logging.debug("str_or({}, {})".format(val, mask))

    val_s = bin(val)[2:]
    logging.debug("val {} : {}".format(val, val_s))

    #prepend with 0s to match mask len
    val_s = "0" * (len(mask) - len(val_s)) + val_s
    logging.debug("val prepend: {}".format(val_s))

    for i in range(len(mask)):
        if mask[i] == 'X':
            result += 'X'
        elif mask[i] == '1':
            result += '1'
        else:
            result += val_s[i]

        logging.debug("  i: {}  mask[i]: {}  result: {}".format(i, mask[i], result))

    return result



def findregs(mask, n, regs):

    logging.debug("  Find registers for: {}, {}".format(mask, n))

    if (len(mask) == n):
        regs.append(int(mask, 2))
        logging.debug("  At the end; update regs: {}".format(regs))

    elif mask[n] == 'X':
        findregs(mask[0:n] + '0' + mask[n+1:], n+1, regs)
        findregs(mask[0:n] + '1' + mask[n+1:], n+1, regs)
    else:
        findregs(mask, n+1, regs)


def part2(data):

    memory = {}
    mask = ""
    regs = []

    for step in data:
        if 'mask' in step:
            mask = step['mask']['maskdata']
            logging.debug ("Updated mask to {}".format(mask))
        else:
            regbase = int(step['index'])
            regbase = str_or(regbase, mask)
            regs = []
            findregs(regbase, 0, regs)
            logging.info ("regbase {} generates regs: {}".format(regbase, regs))
            for reg in regs:
                memory[reg] = int(step['value']);
                logging.debug ("Updated mem[%d] to %d" % (reg, memory[reg]))

    logging.debug ("Memory when done: {}".format(memory))
    thesum = 0
    for key,val in memory.items():
        thesum += val

    return thesum
  
def part1(data):

    memory = {}
    mask = {}

    for step in data:
        if 'mask' in step:
            mask = step['mask']
            logging.debug ("Updated mask to {}".format(mask))
        else:
            i = int(step['index'])
            orig = memory.get(i,0)
            val = int(step['value'])
            memory[i] = (val & mask['andmask']) | mask['ormask']
            logging.debug ("Updated mem[%d] from %d to %d" % (i, val, memory[i]))

    logging.debug ("Memory when done: {}".format(memory))
    thesum = 0
    for key,val in memory.items():
        thesum += val
        logging.debug (" sum adds %d (from %d): %d" % (val, key, thesum))

    return thesum

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    departure = 0
    data = []

    re_mask = re.compile(r"mask = (?P<mask>\w+)$")
    re_data = re.compile(r"mem\[(?P<index>\d+)\][\s=]+(?P<value>\d+)$")
    for line in fileinput.input():
        if ("mask" in line):
            #mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
            maskdata = re_mask.match(line).groupdict()['mask']
            data.append({'mask': {'maskdata': maskdata, 'ormask' : int(maskdata.replace('X', '0'), 2), 'andmask' : int(maskdata.replace('X', '1'), 2) }})
        else:
            # mem[7] = 101
            data.append(re_data.match(line).groupdict())
    logging.debug("data: {0}".format(data))

    #result = part1(data)
    #print("Part1: %d" % result)
    result = part2(data)
    print("Part2 {0}".format(result))
