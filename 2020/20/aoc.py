#!/usr/bin/python

import logging
import sys
import fileinput
import time
import math
import re
from itertools import combinations 
from itertools import permutations 
  
def sig(edge):
    # convert the edge into a signature
    val = 0
    for i in range(len(edge)):
        if edge[i] == '#':
            val += pow(2,i)
    logging.debug("{} : {}".format(edge,val))
    return val

def showtile(tile):
    
    s = "\n"
    for row in tile['data']:
        for col in row:
            s += col
        s += "\n"
    logging.debug(s)
        
def validate(data, order):

    perms = permutations(order)


def part1(data):

    #perms = permutations(tiles)
    #for each in perms:
    #    validate(data, each)
    #    logging.debug("  {}".format(each))

    # map sig values -> list of tiles with those
    # any sig values with 1 tile must be edge
    # any tiles with 2 sigs of a single occurrence must be a corner

    sigmap = {}
    for d in data:
        for sig in d['sig']:
            if sig in sigmap:
                sigmap[sig].add(d['tile'])
            else:
                sigmap[sig] = set([d['tile']])

    for d in data:
        d['common_edges'] = 0
        for sig in d['sig']:
            d['common_edges'] += (len(sigmap[sig]) - 1)

    for d in data:
        logging.debug("tile {}: {} common edges".format(d['tile'], d['common_edges']))


    return 0

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    tilepat = re.compile(r"^Tile ([\d]+):")

    tilenum = 0
    data = []
    data.append({'data': []})

    for line in fileinput.input():
        #logging.debug("len: {}  line:{}".format(len(line), line))
        match = tilepat.match(line)
        if match:
            data[tilenum]['tile'] = match.group(1)
            continue
        if len(line) < 2:
            tilenum += 1
            data.append({'data': []})
            continue

        data[tilenum]['data'].append(list(line.rstrip()))

    for each in data:
        showtile(each)
        each['sig'] = [sig(each['data'][0])]
        each['sig'].append(sig([i[-1] for i in each['data']]))
        each['sig'].append(sig(each['data'][len(each['data'])-1]))
        each['sig'].append(sig([i[0] for i in each['data']]))

    logging.debug("Data: {}".format(data))
    result = part1(data)
    print("Part1: %d" % result)
    #result = part2(data)
    #print("Part2 {0}".format(timestamp))
