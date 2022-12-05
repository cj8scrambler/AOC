#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 
  
play = [ 'invalid', 'rock', 'paper', 'scissor']
results = [ 'invalid', 'loose', 'tie', 'win']

def round_score(them, me):

    t = ord(them) - (ord('A') - 1)
    m = ord(me) - (ord('X') - 1)
    #logging.debug("them: {} ({})  me: {} ({})".format(play[t], them, play[m], me))
    
    if t == m:
        logging.debug("  tie: {} total: {}".format(3, m+3))
        return m+3
    elif (m == t + 1) or (m == 1 and t == 3):
        logging.debug("  win: {} total: {}".format(6, m+6))
        return m+6

    logging.debug("  loose: {} total: {}".format(0, m+0))
    return m

def strategy1(data):

    total = 0

    for line in data:
        [them, me] = line.split()
        total += round_score(them, me)

    return(total)

def right_move(them, result):
    t = ord(them) - (ord('A') - 1)
    r = ord(result) - (ord('X') - 1)
    logging.debug("them: {} ({})  result: {} ({})".format(play[t], them, results[r], result))

    #draw:
    if result == 'Y':
        m = t

    #loose
    elif result == 'X':
        m = t - 1
        if m == 0:
            m = 3
        logging.debug("  loose with: {} [{}]".format(play[m], m))
    # win
    else:
        m = t + 1
        if m == 4:
            m = 1
        logging.debug("  win with: {} [{}]".format(play[m], m))

    me = chr(m+ord('X')-1)
    logging.debug("  my move to {}: {} ({}) [{}]".format(results[r], play[m], me, m))
    return me

def strategy2(data):

    total = 0

    for line in data:
        [them, result] = line.split()
        me = right_move(them, result)
        total += round_score(them, me)

    return(total)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line for line in fileinput.input()]

    before = time.time()
    result = strategy1(lines)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = strategy2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))
