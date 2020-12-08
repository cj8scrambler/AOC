#!/usr/bin/python

import logging
import sys
import fileinput
import time
import copy
from itertools import combinations 
  
def showme(data):
    for line in data:
        logging.info("{0}".format(line))

def op(instructions, pc, acc):
    (opcode, operand) = instructions[pc]
    #logging.debug("got opcode '%s'  operand '%d'" % (opcode, operand))

    #erase that instruction so we know if we hit it again later
    instructions[pc] = ('hlt', 0)

    if opcode == 'nop':
        pc += 1
        logging.debug("got nop: acc=%d, pc=%d" % (acc, pc))
    if opcode == 'acc':
        acc += operand
        pc += 1
        logging.debug("got acc: acc=%d, pc=%d" % (acc, pc))
    if opcode == 'jmp':
        pc += operand
        logging.debug("got jmp: acc=%d, pc=%d" % (acc, pc))
    if opcode == 'hlt':
        pc = -1
        logging.debug("got hlt: acc=%d, pc=%d" % (acc, pc))

    return (acc, pc)

def run(instructions):
    acc = 0
    pc = 0
    while pc >= 0 and pc < len(instructions):
        (acc, pc) = op(instructions, pc, acc)

    return (acc, pc)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    data = []
    for line in fileinput.input():
        e = line.split()
        data.append((e[0],int(e[1])))

    showme(data)

    (acc, pc) = run(copy.copy(data))
    print ("Part 1: acc=%d" % (acc));

    for guess in range(len(data)):
        (opcode, operand) = data[guess]
        logging.debug("line %d: %s,%d" % (guess, opcode, operand))
        new = []
        if opcode == 'nop':
            new = copy.copy(data)
            new[guess] = ('jmp', operand)
            logging.debug("Update line {0} to: {1}".format(guess, new[guess]))
        if opcode == 'jmp':
            new = copy.copy(data)
            new[guess] = ('nop', operand)
            logging.debug("Update line {0} to: {1}".format(guess, new[guess]))
        if (len(new)):
            logging.debug("Run new simulation for line {0}".format(guess))
            (acc,pc) = run(new)
            if (pc == len(new)):
                print("Program completed succesfully by updating line %d; acc=%d" % (guess, acc))
                break
