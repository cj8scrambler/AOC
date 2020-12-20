#!/usr/bin/python3

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
  
def domath1(input, begin):

    last = None
    operand = None
    val = None

    logging.debug("domath({})".format(input[begin:]))
    i = begin
    while i < len(input):
        logging.debug("Working on pos {}: {}".format(i, input[i]))
        if input[i] == '+' or input[i] == '*':
            operand = input[i]
        elif input[i] == '(':
            logging.debug("  recurse on: {}".format(input[i+1:]))
            if last:
                (i, val) = domath1(input, i+1)
            else:
                (i, last) = domath1(input, i+1)
            logging.debug("  recurse returned: ({},{})".format(i, val))
        elif input[i] == ')':
            logging.debug("At ')'; return ({},{})".format(i,last));
            return (i, last)
        else:
            try:
                tmp = int(input[i])
                if last:
                    val = tmp
                else:
                    last = tmp
            except ValueError:
                logging.error("NAN: What to do with: {}".format(input[i]))

        if operand and val:
            if operand == '+':
                logging.info("Execute: {} {} {} = {}".format(last, operand, val, last+val))
                last += val
            elif operand == '*':
                logging.info("Execute: {} {} {} = {}".format(last, operand, val, last*val))
                last *= val

            operand = None
            val = None

            logging.debug("result: {}".format(last))
        else:
            logging.debug("waiting for more")

        i += 1

    logging.info("return {}".format(last))
    return (0, last)

def part1(data):

    sum = 0
    for each in data:
        (i, val) = domath1(each, 0)
        sum += val
        logging.error(" result: {}  sum: {}  from: {}".format(val, sum, each))
    return sum

def domath2(input, begin):

    vals = []
    ops = []

    logging.debug("domath({})".format(input[begin:]))
    i = begin
    while i < len(input):
        logging.debug("Working on pos {}: {}".format(i, input[i]))
        if input[i] == '+':
            ops.append(input[i])
        elif input[i] == '*':
            if len(ops) and ops[-1] == '+':
                logging.debug("  Encountered lower precedent operator: resolve previous ones first")
                while len(ops) and ops[-1] == '+':
                    op = ops.pop()
                    logging.debug("    {} + {} = {}".format(vals[-1], vals[-2], vals[-1] + vals[-2]))
                    vals.append(vals.pop() + vals.pop())
            ops.append(input[i])
        elif input[i] == '(':
            logging.debug("    recurse on: {}".format(input[i+1:]))
            (i, tmp) = domath2(input, i+1)
            vals.append(tmp)
            logging.debug("    recurse returned: ({},{})".format(i, tmp))
        elif input[i] == ')':
            logging.debug("  At ')'; execute stack; vals: {}  ops: {}".format(vals, ops))
            while(len(ops)):
                op = ops.pop()
                if (op == '+'):
                    logging.debug("    {} + {} = {}".format(vals[-1], vals[-2], vals[-1] + vals[-2]))
                    vals.append(vals.pop() + vals.pop())
                elif (op == '*'):
                    logging.debug("    {} * {} = {}".format(vals[-1], vals[-2], vals[-1] * vals[-2]))
                    vals.append(vals.pop() * vals.pop())
                else:
                    raise ValueError
            logging.debug("    finished ops; return []  vals: {}".format(vals[0], vals))
            return (i, vals[0])
        else:
            try:
                vals.append(int(input[i]))
            except ValueError:
                logging.error("  NAN: What to do with: {}".format(input[i]))
        logging.debug("  Now val: {}  ops: {}".format(vals,ops))
        i += 1

    logging.debug("done parsing; execute stack; vals: {}  ops: {}".format(vals, ops))
    while(len(ops)):
        op = ops.pop()
        if (op == '+'):
            logging.debug("  {} + {} = {}".format(vals[-1], vals[-2], vals[-1] + vals[-2]))
            vals.append(vals.pop() + vals.pop())
        elif (op == '*'):
            logging.debug("  {} * {} = {}".format(vals[-1], vals[-2], vals[-1] * vals[-2]))
            vals.append(vals.pop() * vals.pop())
        else:
            raise ValueError
    logging.debug("  finished ops; return []  vals: {}".format(vals[0], vals))
    return (0, vals[0])

def part2(data):

    sum = 0
    for each in data:
        (i, val) = domath2(each, 0)
        sum += val
        logging.error(" result: {}  sum: {}  from: {}".format(val, sum, each))
    return sum


if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    rules = []
    tickets = []   # my ticket is first

    on_rules = True

    data = []
    #data = [list(line.rstrip()) for line in fileinput.input()]
    for line in fileinput.input():
        l = [i.strip() for i in list(line.rstrip())]
        data.append([j for j in l if j != ''])

    logging.debug("Data: {}".format(data))

    #result = part1(data)
    #print("Part 1: {}".format(result))

    result = part2(data)
    print("Part 2: {}".format(result))
