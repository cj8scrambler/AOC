#!/usr/bin/python3

import logging
import sys
import fileinput
import time
import math
import re
import copy
from itertools import combinations 
from itertools import permutations 

def find_n(subject, public_key):

    ans = 0
    val = 1
    while val != public_key:
        ans += 1
        #logging.debug("i {}:  ({} * {}) % 20201227 = {}".format(ans, subject, val, (subject*val) % 20201227))
        val = (subject * val) % 20201227

    return ans

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    #-- Example ---
    subject = 7
    pubkey1 = 5764801
    pubkey2 = 17807724

    subject = 7
    pubkey1 = 8335663
    pubkey2 = 8614349

    #logging.debug("subject: 7  iter: 8  result: {}".format(iter(7, 8)))
    n1 = find_n(subject, pubkey1)
    logging.info("n1: {}".format(n1))
    n2 = find_n(subject, pubkey2)
    logging.info("n2: {}".format(n2))

    print("Encryption key 1: {}".format(pow(pubkey1, n2) % 20201227))
    print("Encryption key 2: {}".format(pow(pubkey2, n1) % 20201227))
    #result = part1(data, 100)
    #print("Part1: {}".format(result))
