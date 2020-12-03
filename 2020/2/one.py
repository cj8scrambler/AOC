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
    logging.debug("%c occurs %d times in '%s'" % (password['char'], oc, password['pass']))
    if (oc >= int(password['min'])) and (oc <= int(password['max'])):
        return True

    return False


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    # 1-3 a: abcde
    pattern = re.compile(r"(?P<min>\d+)-(?P<max>\d+)\s*(?P<char>\w):\s*(?P<pass>\w+$)")

    data = [pattern.match(line).groupdict() for line in fileinput.input()]

    #showme(data)
    valid = 0;
    for entry in data:
        valid += validate(entry)

    print("%d valid passwords" % (valid))
