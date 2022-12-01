#!/usr/bin/python

import logging
import sys
import fileinput
import csv
import time
import re
from functools import reduce


def trimrange((rlow,rhigh), (trimlow,trimhigh)):
    if (rlow > trimhigh):
        logging.debug("trim range: {} to: {}".format((rlow,rhigh), []))
        return []
    if (rhigh < trimlow):
        logging.debug("trim range: {} to: {}".format((rlow,rhigh), []))
        return []

    low = min(max(rlow,trimlow), trimhigh)
    high = max(min(rhigh,trimhigh), trimlow)

    logging.debug("trim range: {} to: {}".format((rlow,rhigh), (low,high)))
    return range(low,high)

def part1(data, limits):
    results = {}

    for val, (xmin,xmax),(ymin,ymax),(zmin,zmax) in data:
        logging.info("On line: V: {}  X: {}-{}  Y: {}-{}  Z: {}-{}".format(val, xmin, xmax, ymin, ymax, zmin, zmax))
        for x in trimrange((xmin, xmax+1), limits):
            for y in trimrange((ymin, ymax+1), limits):
                for z in trimrange((zmin, zmax+1), limits):
                    results[(x,y,z)] = val
                    logging.debug("  set results[{}]: {}".format((x,y,z), val))
        logging.info("  {}/{} on".format(sum(results.values()), len(results)))


    s = sum(results.values())
    logging.info("{} elements on".format(s))
    return s


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    for line in fileinput.input():
        #on x=10..12,y=10..12,z=10..12
        #g = re.match( r"^on x=(/d+)..(/d+),y=(/d+)..(/d+),z=(/d+)..(/d+)$", line)
        #g = re.match( r"^on x=([0-9]+)\.\.([0-9]+)", line)
        g = re.match( r"^(.*) x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)", line)
        if g:
            if g.group(1) == 'on':
                o = 1
            elif g.group(1) == 'off':
                o = 0
            else:
                raise("Invalid")
            data.append((o, (int(g.group(2)),int(g.group(3))), (int(g.group(4)),int(g.group(5))), (int(g.group(6)),int(g.group(7)))))
        else:
            logging.error("No match on line: {}".format(line))

    logging.debug("data: {}".format(data))

    before = time.time()
    result = part1(data, (-50,50))
    after = time.time()
    print("part 1 result: {}".format(result))
