#!/usr/bin/python

import logging
import sys
import fileinput
import time
  
def part1(data, count):
    
    gamma_s =""
    epsilon_s =""

    for bit in data:
        if bit < count/2:
            gamma_s += "0"
            epsilon_s += "1"
        if bit > count/2:
            gamma_s += "1"
            epsilon_s += "0"
        if bit == count/2:
            raise ValueError("it's a tie")
        logging.debug("gamma_s: {}".format(gamma_s))
        logging.debug("epsilon_s: {}".format(epsilon_s))

    gamma = int(gamma_s,2)
    epsilon = int(epsilon_s,2)
    logging.debug("gamma: {}   epsilon: {}  product: {}".format(gamma, epsilon, gamma*epsilon))
    return((gamma,epsilon))

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    bitcounts = []
    linecount = 0
    for line in fileinput.input():
        while len(data) < len(line.rstrip()):
            data.append([])
            bitcounts.append(0)
        for i in range(len(line.rstrip())):
            logging.debug("line[{}]: {}".format(i, line[i]))
            data[i].append(int(line[i]))
            bitcounts[i] += int(line[i])
        linecount += 1

    logging.debug("Got data for {} lines: {}".format(linecount, data))

    before = time.time()
    (gamma,epsilon) = part1(bitcounts, linecount)
    after = time.time()
    print("part 1 product: {} ({:.3f} sec)".format(gamma*epsilon, (after - before)))
