#!/usr/bin/python

import logging
import sys
import fileinput
import csv

def execute(data, pc):
    if (data[pc] == 1):
        logging.debug ("pc: %d  opcode: %d (+) : %d + %d => [%d]" % (pc, data[pc], data[data[pc+1]], data[data[pc+2]], data[pc+3]))
        data[data[pc+3]] = data[data[pc+1]] + data[data[pc+2]]
        return (pc+4)
    elif (data[pc] == 2):
        logging.debug ("pc: %d  opcode: %d (*) : %d * %d => [%d]" % (pc, data[pc], data[data[pc+1]], data[data[pc+2]], data[pc+3]))
        data[data[pc+3]] = data[data[pc+1]] * data[data[pc+2]]
        return (pc+4)
    elif (data[pc] == 99):
        logging.debug ("pc: %d  opcode: %d (DONE)" % (pc, data[pc]))
        return (pc+1);
    else:
        logging.debug ("pc: %d  opcode: %d  INVALID" % (pc, data[pc]))
        raise RuntimeError("Unkown opcode at address %d: %d" % (pc, data[pc]))

def day2_part2(memory):
    for noun in range(100):
        for verb in range(100):
            data = list(memory) #make a copy
            data[1] = noun
            data[2] = verb
            pc = 0
            logging.debug ("Program Data: %s" % (data))
            while data[pc] != 99:
                pc = execute(data, pc)

            if data[0] == 19690720:
                print("Found solution: %d  noun=%d  verb=%d  answer=%d" % (data[0], noun, verb, noun*100+verb))
            else:
                logging.debug("Nope: %d" % (data[0]))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    with open(sys.argv[1], 'r') as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            row = [int(i) for i in row]
            print("Day 2 part 2")
            day2_part2(row)
