#!/usr/bin/python

import sys
import fileinput

i = 0
sum = 0

def execute(data, pc):
    if (data[pc] == 1):
        print ("pc: %d  opcode: %d : %d + %d => [%d]" % (pc, data[pc], data[data[pc+1]], data[data[pc+2]], data[pc+3]))
        data[data[pc+3]] = data[data[pc+1]] + data[data[pc+2]]
        return (pc+4)
    elif (data[pc] == 2):
        print ("pc: %d  opcode: %d : %d * %d => [%d]" % (pc, data[pc], data[data[pc+1]], data[data[pc+2]], data[pc+3]))
        data[data[pc+3]] = data[data[pc+1]] * data[data[pc+2]]
        return (pc+4)
    elif (data[pc] == 99):
        print ("pc: %d  opcode: %d  DONE" % (pc, data[pc]))
        return (pc);
    else:
        print ("pc: %d  opcode: %d  INVALID" % (pc, data[pc]))
        return (100000000000000000000);

with open(sys.argv[1], 'r') as data:
    for line in data:
        data = line.rstrip().split(",")
        data = [int(i) for i in data]
        pc = 0
        print (data)
        while data[pc] != 99:
            pc = execute(data, pc)
        if (data[pc] == 99):
            print("Success:")
            print(data)
        else:
            print("Fail")
            print(data)
