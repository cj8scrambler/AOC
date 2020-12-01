#!/usr/bin/env python3

import logging
import sys
import fileinput
import csv
import queue
import threading
from itertools import permutations

def execute(data, pc, inq, outq):
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
        logging.debug ("pc: %d  opcode: %d (i) : wait for queue input" % (pc, opcode))
        data[data[pc+1]] = inq.get()
        print('Input: %s' % (data[data[pc+1]]));
        logging.debug ("pc: %d  opcode: %d (i) : %d => [%d]" % (pc, opcode, data[data[pc+1]], data[pc+1]))
        return (pc+2)
    elif (opcode == 4):
        if arg[1]:
            arg1 = data[pc+1]
        else:
            arg1 = data[data[pc+1]]
        logging.debug ("pc: %d  opcode: %d (o) : %d" % (pc, opcode, arg1))
        outq.put(arg1)
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

def day7_part2(memory, indata, outdata):

    print("DZ: Begin");
    pc = 0
    logging.debug ("Program Data: %s" % (memory))
    while memory[pc] != 99:
        pc = execute(memory, pc, indata, outdata)
    return (outval)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    best_thrust=0
    atnum = 0
    threads = [None] * 5 
    #for attempt in permutations(range(5), 5):
    for attempt in [[0, 1, 2, 3, 4]]:
        thrust = 0
        print("Attempt: %d (%s)  Thrust: %d" % (atnum, attempt, thrust))
        atnum += 1
        q = [queue.Queue() for i in range(len(attempt) + 1) ]
        print("DZ: threads: %s\n" % (threads))
        print("DZ: q: %s\n" % (q))
        qnum = 0
        q[qnum].put(0)
        for step in attempt:
            with open(sys.argv[1], 'r') as csvfile:
                for row in csv.reader(csvfile, delimiter=','):
                    row = [int(i) for i in row]
                    #thrust = day7_part2(row, q[qnum], q[qnum+1] )
                    print("DZ: creating thread=%d  inQ=%d outQ=%d\n" % (qnum, qnum, qnum+1))
                    threads[qnum] = threading.Thread(target=day7_part2, args=(row, q[qnum], q[qnum+1]))
                    threads[qnum].start()
            qnum += 1
        for t in threads:
            t.join()

        for each in q:
            print("DZ: Done: Q size: %d" % (each.qsize()))
        thrust = q[len(attempt)].get

        if thrust > best_thrust:
            best_thrust = thrust
            logging.debug("Attempt %d new best: %s" % (atnum, best_thrust))

    print("Best thrust: %d" % (best_thrust))
