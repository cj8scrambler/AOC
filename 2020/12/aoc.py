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

def move(loc, direction, amount):
    if direction == 'N':
        loc['y'] += amount
    if direction == 'S':
        loc['y'] -= amount
    if direction == 'E':
        loc['x'] += amount
    if direction == 'W':
        loc['x'] -= amount
        
    #return loc

def part1(data):

    loc = {'heading': 90, 'x': 0, 'y': 0}
    dlookup = dict([(0, 'N'), (90, 'E'), (180, 'S'), (270, 'W')])
    for step in data:
        #logging.debug(" step: {0}".format(step))
        if step['direction'] == 'L':
            loc['heading'] = (loc['heading'] - int(step['value'])) % 360
            logging.debug("  cmd 'L': heading: %d" % (loc['heading']))
        elif step['direction'] == 'R':
            loc['heading'] = (loc['heading'] + int(step['value'])) % 360
            logging.debug("  cmd 'R': heading: %d" % (loc['heading']))
        elif step['direction'] == 'F':
            logging.debug("  cmd 'F': dir '%c' move '%d'" % (dlookup[loc['heading']], int(step['value'])))
            loc = move(loc, dlookup[loc['heading']], int(step['value']))
        else:
            logging.debug("  cmd '%c': move '%d'" % (step['direction'], int(step['value'])))
            loc = move(loc, step['direction'], int(step['value']))
        logging.debug(" now: [%d,%d] (%c)" % (loc['x'], loc['y'], dlookup[loc['heading']]))

    mh = abs(loc['x'])+abs(loc['y'])
    logging.debug(" final: [%d,%d] : %d" % (loc['x'], loc['y'], mh))
    return mh

def rotate(xy, direction, times):
    for i in range(times):
        logging.debug("  #{0}: before: {1}".format(i, xy))
        oldy=xy['y']
        xy['y'] = xy['x']
        xy['x'] = oldy
        if (direction == 'L'):
            xy['x'] *= -1
        if (direction == 'R'):
            xy['y'] *= -1
        logging.debug("  #{0}: after: {1}".format(i, xy))

def part2(data):

    wp = {'x': 10, 'y': 1}
    loc = {'x': 0, 'y': 0}
#    dlookup = dict([(0, 'N'), (90, 'E'), (180, 'S'), (270, 'W')])
    for step in data:
        #logging.debug(" step: {0}".format(step))
        if step['direction'] == 'L' or step['direction'] == 'R':
            rotate(wp, step['direction'], abs(int(step['value']))/90)
            logging.debug("  cmd '{0}{1}':   wp: {2}".format(step['direction'], step['value'], wp))
        elif step['direction'] == 'F':
            logging.debug("  cmd 'F': move {0} times towards {1}".format(step['value'], wp))
            for i in range(int(step['value'])):
                loc['x'] += wp['x']
                loc['y'] += wp['y']
                logging.debug("    f step #{0}: {1}  [wp: {2}]".format(i, loc, wp))
        else:
            logging.debug("  cmd '%c': move '%d'" % (step['direction'], int(step['value'])))
            move(wp, step['direction'], int(step['value']))
        logging.debug(" now  ship: [%d,%d]  wp: [%d,%d]" % (loc['x'], loc['y'], wp['x'], wp['y']))

    mh = abs(loc['x'])+abs(loc['y'])
    logging.debug(" final: [%d,%d] : %d" % (loc['x'], loc['y'], mh))
    return mh


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    # 1-3 a: abcde
    pattern = re.compile(r"^(?P<direction>\w)(?P<value>\d+)$")

    data = [pattern.match(line).groupdict() for line in fileinput.input()]

    showme(data)
    #result = part1(data)
    #print("Part1 MD: %d" % result)
    result = part2(data)
    print("Part2 MD: %d" % result)
