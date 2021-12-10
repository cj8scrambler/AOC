#!/usr/bin/python

import logging
import sys
import fileinput
import csv

relbase = 0

def arg_write_addr(data, pc, argnum, argtype):
    global relbase

    if argtype == 0:
        return data[pc+argnum]
    elif argtype == 2:
        return relbase + data[pc+argnum]

    raise RuntimeError("Invalid addressing mode for arg-{}: {}".format(argnum, argtype))

def arg_read_val(data, pc, argnum, argtype):

    if argtype == 0:
        logging.debug("  arg-{} mode-0 (indirect) data[data[{}+{}]] == data[{}]: {}".format(argnum, pc, argnum, data[pc+argnum], data[data[pc+argnum]]))
        return data[data[pc+argnum]]
    elif argtype == 1:
        logging.debug("  arg-{} mode-1 (immediate) data[{}+{}]: {}".format(argnum, pc, argnum, data[pc+argnum]))
        return data[pc+argnum]
    elif argtype == 2:
        logging.debug("  arg-{} mode-2 (relbase) data[{} + data[{}+{}]] == data[{}]: {}".format(argnum, relbase, pc, argnum, relbase + data[pc+argnum], data[relbase+data[pc+argnum]]))
        return data[relbase + data[pc+argnum]]

    raise RuntimeError("Invalid addressing mode for arg-{}: {}".format(argnum, argtype))

def execute(data, pc):
    global relbase
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
    logging.debug ("pc: %d  value: %d  opcode: %d  arg1: %d  arg2: %d  arg3 %d" % (pc, data[pc], opcode, arg[1], arg[2], arg[3]))

    # +
    if (opcode == 1):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        arg2 = arg_read_val(data, pc, 2, arg[2])
        arg3 = arg_write_addr(data, pc, 3, arg[3])
        logging.debug ("pc: %d    opcode: %d (+) : %d + %d => [%d]" % (pc, opcode, arg1, arg2, arg3))
        data[arg3] = arg1 + arg2
        return (pc+4)

    # *
    elif (opcode == 2):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        arg2 = arg_read_val(data, pc, 2, arg[2])
        arg3 = arg_write_addr(data, pc, 3, arg[3])
        logging.debug ("pc: %d    opcode: %d (*) : %d + %d => [%d]" % (pc, opcode, arg1, arg2, arg3))
        data[arg3] = arg1 * arg2
        return (pc+4)

    # Input
    elif (opcode == 3):
        arg1 = arg_write_addr(data, pc, 1, arg[1])
        val = input('Input: ');
        data[arg1] = val;
        logging.debug ("pc: %d    opcode: %d (i) : %d => [%d]" % (pc, opcode, val, arg1))
        return (pc+2)

    # Output
    elif (opcode == 4):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        logging.debug ("pc: %d    opcode: %d (o) : %d" % (pc, opcode, arg1))
        print('Output: %s' % (arg1));
        return (pc+2)

    # jump if true
    elif (opcode == 5):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        arg2 = arg_read_val(data, pc, 2, arg[2])
        logging.debug ("pc: %d    opcode: %d (JT) : %d => [%d]" % (pc, opcode, arg1, arg2))
        if (arg1):
            logging.debug ("    jump to %d" % (arg2))
            pc = arg2;
            return (pc)
        return (pc+3)

    # jump if false
    elif (opcode == 6):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        arg2 = arg_read_val(data, pc, 2, arg[2])
        logging.debug ("pc: %d    opcode: %d (JF) : %d => [%d]" % (pc, opcode, arg1, arg2))
        if (arg1 == 0):
            logging.debug ("    jump to %d" % (arg2))
            pc = arg2;
            return (pc)
        return (pc+3)

    # less than
    elif (opcode == 7):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        arg2 = arg_read_val(data, pc, 2, arg[2])
        arg3 = arg_write_addr(data, pc, 3, arg[3])
        logging.debug ("pc: %d    opcode: %d (LT) : %d ?< %d => [%d]" % (pc, opcode, arg1, arg2, data[pc+3]))
        if (arg1 < arg2):
            data[arg3] = 1
        else:
            data[arg3] = 0
        return (pc+4)

    # == 
    elif (opcode == 8):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        arg2 = arg_read_val(data, pc, 2, arg[2])
        arg3 = arg_write_addr(data, pc, 3, arg[3])
        logging.debug ("pc: %d    opcode: %d (==) : %d ?= %d => [%d]" % (pc, opcode, arg1, arg2, data[pc+3]))
        if (arg1 == arg2):
            data[arg3] = 1
        else:
            data[arg3] = 0
        return (pc+4)

    # relative base
    elif (opcode == 9):
        arg1 = arg_read_val(data, pc, 1, arg[1])
        relbase += arg1
        logging.debug ("pc: %d    opcode: %d (relbase) : %d" % (pc, opcode, arg1))
        return (pc+2)

    # halt
    elif (opcode == 99):
        logging.debug ("pc: %d    opcode: %d (DONE)" % (pc, data[pc]))
        return (pc+1);
    else:
        logging.debug ("pc: %d    opcode: %d  INVALID" % (pc, data[pc]))
        raise RuntimeError("Unkown opcode at address %d: %d" % (pc, data[pc]))

def part1(memory):
    pc = 0
    memoffset = len(memory)
    memory.extend([0] * 2000)
    logging.debug ("Program Data ({}): {}".format(len(memory),memory))
    while memory[pc] != 99:
        pc = execute(memory, pc)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    with open(sys.argv[1], 'r') as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            row = [int(i) for i in row]
            part1(row)
