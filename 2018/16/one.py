#!/usr/bin/python

import sys
import re
import numpy as np
import Gnuplot
import operator

before = [0] * 4
ins = [0] * 4
result = [0] * 4
after = [0] * 4

opcodes = [
 { 'name': 'addr', 'operands' : [1, 1, 1], 'operator': operator.add},
 { 'name': 'addi', 'operands' : [1, 0, 1], 'operator': operator.add},
]

#(possible, result) = run_opc(opcode, before)
def run_opc(opcode, args, registers):
    ``` return (possible, [result]) ```
    if opcode['operands'][0]:
        vala = args[1]
    else
        if (args[1] <= 4):
            vala = before[args[1]]
        else:
            return (0, [0,0,0,0])
    if opcode['operands'][1]:
        valb = args[2]
    else
        if (args[2] <= 4):
            valb = before[args[2]]
        else:
            return (0, [0,0,0,0])


with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        if 'Before' in source:
            g = re.match( r"Before:[ ]+\[(-?[0-9]+), (-?[0-9]+), (-?[0-9]+), (-?[0-9]+)\]", source)
            if g:
                before[0] = int(g.group(1))
                before[1] = int(g.group(2))
                before[2] = int(g.group(3))
                before[3] = int(g.group(4))
                print("got a before: %s" % (before))
        elif 'After' in source:
            g = re.match( r"After:[ ]+\[(-?[0-9]+), (-?[0-9]+), (-?[0-9]+), (-?[0-9]+)\]", source)
            if g:
                after[0] = int(g.group(1))
                after[1] = int(g.group(2))
                after[2] = int(g.group(3))
                after[3] = int(g.group(4))
                print("got a after: %s" % (after))
                match = 0 
            for opcode in opcodes:
                (possible, result) = run_opc(opcode, ins, before)
                if (possible and (result == after)):
                    print ("opcode: %s(%s) => %s" % (opcode, before, result))
                    match += 1 
        else:
            ins = list(map(int, source.split()))
            print("got a inst: %s" % (ins))
