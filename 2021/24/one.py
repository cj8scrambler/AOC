#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
from functools import reduce


def part1(data):

    w = 14
    best = 0
    #for sernum in range(int('1'*w), pow(10,w)):
    for sernum in range(pow(10,w)-1, 0, -1):
        inp = []
        for d in str(sernum).zfill(w):
            if d == '0':
                inp = []
                break
            else:
                inp.append(int(d))
        if len(inp):
            logging.debug("{}: call execute with data: {}".format(sernum,inp))
            result = execute(data, inp)
            logging.info("{}: {}".format(sernum,result))
            if result == 0:
                return sernum

def execute(data, inp_data):

    regs = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    for ins in data:
        arg3 = None
        if len(ins) == 3:
            if type(ins[2]) is int:
                arg3 = ins[2]
            else:
                arg3 = regs[ins[2]]

        if ins[0] == 'inp':
            if inp_data:
                regs[ins[1]] = inp_data.pop(0)
            else:
                regs[ins[1]] = int(input("input value: "))
            logging.debug("{}: input: {} -> {}".format(ins, regs[ins[1]], ins[1]))
        elif ins[0] == 'add':
            logging.debug("{}: {}({}) + {}({}) = {}".format(ins, ins[1], regs[ins[1]], ins[2], arg3, regs[ins[1]] + arg3))
            regs[ins[1]] = regs[ins[1]] + arg3
        elif ins[0] == 'mul':
            logging.debug("{}: {}({}) * {}({}) = {}".format(ins, ins[1], regs[ins[1]], ins[2], arg3, regs[ins[1]] * arg3))
            logging.debug("  {} * {} = {}".format(regs[ins[1]], arg3,  regs[ins[1]] * arg3))
            regs[ins[1]] = regs[ins[1]] * arg3
        elif ins[0] == 'div':
            logging.debug("{}: {}({}) / {}({}) = {}".format(ins, ins[1], regs[ins[1]], ins[2], arg3, regs[ins[1]] / arg3))
            regs[ins[1]] = regs[ins[1]] * arg3
            regs[ins[1]] = regs[ins[1]] / arg3
        elif ins[0] == 'mod':
            logging.debug("{}: {}({}) % {}({}) = {}".format(ins, ins[1], regs[ins[1]], ins[2], arg3, regs[ins[1]] % arg3))
            regs[ins[1]] = regs[ins[1]] % arg3
        elif ins[0] == 'eql':
            logging.debug("{}: {}({}) == {}({}) = {}".format(ins, ins[1], regs[ins[1]], ins[2], arg3, regs[ins[1]] == arg3))
            regs[ins[1]] = int(regs[ins[1]] == arg3)
        else:
            raise("Unkown opcode: ".format(ins))

    return regs['z']


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    with open(sys.argv[1]) as inp:
        for line in inp:
            logging.debug("line: {}".format(line))
            args = line.split()
            if len(args) == 3:
                try:
                    arg3 = int(args[2])
                except ValueError:
                    arg3 = args[2]
    
                data.append((args[0], args[1], arg3))
            elif len(args) == 2:
                data.append((args[0], args[1]))
            else:
                logging.error("No match on line: {}".format(line))

    logging.debug("data: {}".format(data))

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {}".format(result))
