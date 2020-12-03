#!/usr/bin/python

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
  
def showme(data):
    for line in data:
        logging.info("  On: {0}".format(line))

def validate(password):
    oc = password['pass'].count(password['char'])
    pos1 = int(password['pos1'])-1
    pos2 = int(password['pos2'])-1
    logging.debug("'%s': pos %d is %c and pos %d is %c" % (password['pass'], pos1+1, password['pass'][pos1], pos2+1, password['pass'][pos2]))
    if (password['pass'][pos1] == password['char']) != (password['pass'][pos2] == password['char']):
        logging.debug("Match")
        return True

    return False


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # 1-3 a: abcde
    pattern = re.compile(r"(?P<pos1>\d+)-(?P<pos2>\d+)\s*(?P<char>\w):\s*(?P<pass>\w+$)")

    data = [pattern.match(line).groupdict() for line in fileinput.input()]

    valid = 0;
    for entry in data:
        valid += validate(entry)

    print("%d valid passwords" % (valid))
