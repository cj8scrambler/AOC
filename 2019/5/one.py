#!/usr/bin/python

import logging
import sys
import fileinput
import csv

def execute(data, pc):
    arg = [0]*4
    arg[0] = str(data[pc]) 
    if len(arg[0]) >= 2:
        opcode = int(arg[0][-2:])
    else:
        opcode = int(arg[0][-1:])
    if len(arg[0]) >= 3:
        arg[1] = int(arg[0][-3])
        if len(arg[0]) >= 4:
            arg[2] = int(arg[0][-4])
            if len(arg[0]) >= 5:
                arg[3] = int(arg[0][-5])
    #logging.debug ("pc: %d  value: %d  opcode: %d  arg1: %d  arg2: %d  arg3 %d" % (pc, data[pc], opcode, arg[1], arg[2], arg[3]))
    if (opcode == 1):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        if arg[2]:
            arg2 = data[pc+2]
        else:
            arg2 = data[data[pc+2]]
        if arg[3]:
            raise RuntimeError("Invalid addressing mode for arg3")

        logging.debug ("pc: %d  opcode: %d (+) : %d + %d => [%d]" % (pc, opcode, arg1, arg2, data[pc+3]))
        data[data[pc+3]] = arg1 + arg2
        return (pc+4)
    elif (opcode == 2):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        if arg[2]:
            arg2 = data[pc+2]
        else:
            arg2 = data[data[pc+2]]
        if arg[3]:
            raise RuntimeError("Invalid addressing mode for arg3")

        logging.debug ("pc: %d  opcode: %d (*) : %d * %d => [%d]" % (pc, opcode, arg1, arg2, data[pc+3]))
        data[data[pc+3]] = arg1 * arg2
        return (pc+4)
    elif (opcode == 3):
        if arg[1]:
            raise RuntimeError("Invalid addressing mode for arg1")
        val = input('Input: ');
        data[data[pc+1]] = val;
        logging.debug ("pc: %d  opcode: %d (i) : %d => [%d]" % (pc, opcode, val, data[pc+1]))
        return (pc+2)
    elif (opcode == 4):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        logging.debug ("pc: %d  opcode: %d (o) : %d" % (pc, opcode, arg1))
        print('Output: %s' % (arg1));
        return (pc+2)
    # jump if true
    elif (opcode == 5):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        if arg[2]:
            arg2 = data[pc+2]
        else:
            arg2 = data[data[pc+2]]
        logging.debug ("pc: %d  opcode: %d (JT) : %d => [%d]" % (pc, opcode, arg1, arg2))
        if (arg1):
            logging.debug ("    jump to %d" % (arg2))
            pc = arg2;
            return (pc)
        return (pc+3)
    # jump if false
    elif (opcode == 6):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        if arg[2]:
            arg2 = data[pc+2]
        else:
            arg2 = data[data[pc+2]]
        logging.debug ("pc: %d  opcode: %d (JF) : %d => [%d]" % (pc, opcode, arg1, arg2))
        if (arg1 == 0):
            logging.debug ("    jump to %d" % (arg2))
            pc = arg2;
            return (pc)
        return (pc+3)
    # less than
    elif (opcode == 7):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        if arg[2]:
            arg2 = data[pc+2]
        else:
            arg2 = data[data[pc+2]]
        if arg[3]:
            raise RuntimeError("Invalid addressing mode for arg3")
        logging.debug ("pc: %d  opcode: %d (LT) : %d ?< %d => [%d]" % (pc, opcode, arg1, arg2, data[pc+3]))
        if (arg1 < arg2):
            data[data[pc+3]] = 1
        else:
            data[data[pc+3]] = 0
        return (pc+4)

    # == 
    elif (opcode == 8):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        if arg[2]:
            arg2 = data[pc+2]
        else:
            arg2 = data[data[pc+2]]
        if arg[3]:
            raise RuntimeError("Invalid addressing mode for arg3")
        logging.debug ("pc: %d  opcode: %d (==) : %d ?= %d => [%d]" % (pc, opcode, arg1, arg2, data[pc+3]))
        if (arg1 == arg2):
            data[data[pc+3]] = 1
        else:
            data[data[pc+3]] = 0
        return (pc+4)

    # halt
    elif (opcode == 99):
        logging.debug ("pc: %d  opcode: %d (DONE)" % (pc, data[pc]))
        return (pc+1);
    else:
        logging.debug ("pc: %d  opcode: %d  INVALID" % (pc, data[pc]))
        raise RuntimeError("Unkown opcode at address %d: %d" % (pc, data[pc]))

def day5_part1(memory):
    pc = 0
    logging.debug ("Program Data: %s" % (memory))
    while memory[pc] != 99:
        pc = execute(memory, pc)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    with open(sys.argv[1], 'r') as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            row = [int(i) for i in row]
            print("Day 2 part 2")
            day5_part1(row)
