#!/usr/bin/python3

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
#from treelib import Node, Tree
#from anytree import Node, RenderTree
  
def showme(data):
    for line in data:
        logging.info("  {0}".format(line))

def find_color(root, bag, color):
    '''
    look for an occurance of `color` under `bag`.  stop and return true
    if found.  Return false if not found
    '''
    total = 0
    match = 0
    if bag == color:
        logging.debug("node '%s' is the color; return true" % (bag))
        return True


    logging.debug("  find_color(root, bag='%s', color='%s')" % (bag,color))
    for child in root[bag]:
        logging.debug("  recruse to '%s'" % (child['color']))
        if find_color(root, child['color'], color):
            return True

    logging.debug("node '%s' has no '%s' children; return false" % (bag, color))
    return False;

def count_part1(data, color):
    count = 0
    for each in data.keys():
        logging.debug("Top level on: {0}".format(each))
        if (each != color): # can't be a top level bag
            val = find_color(data, each, color)
            if val:
                logging.info("Bag: %s contains a '%s' bag (count now %d)" % (each, color, count))
                count += val

    return count

def count_color(root, color):
    total = 0
    #logging.debug("  count_color(root, color='%s')" % (color))
    if (len(root[color])):
        for child in root[color]:
            logging.debug("  '%s' causes recurse on '%s'" % (color, child['color']))
            val = count_color(root, child['color'])
            total += child['num'] * val
            logging.debug("  recurse on '%s' returned %d; times %d => new total: %d" % (child['color'], val, child['num'], total))
    else:
        return 1

    return total + 1;

def count_part2(root, color):
    logging.info("Count bags in %s" % (color))
    val = count_color(data, color) - 1 #don't count yourself

    return val

if __name__ == '__main__':

    logging.basicConfig(level=logging.WARN)

    pat1 = re.compile(r"^([\w]+ [\w]+) bags contain")
    pat2 = re.compile(r".*([\d]+) ([\w]+ [\w]+) bag")

    data = {}
    for line in fileinput.input():
        #logging.debug("line: '%s'" % (line))
        match1 = pat1.match(line)
        if match1:
            top = match1.group(1)
            logging.debug("  create top node: '%s'" % (match1.group(1)))
            data[match1.group(1)] = []
            rest = line[len(top + " bags contain"):].split(',')
            for sub in rest:
                #logging.debug("  sub: '%s'" % (sub))
                match2 = pat2.match(sub)
                if match2:
                    logging.debug("    create child node: '%s'  parent='%s'  data='%d'" % (match2.group(2), match1.group(1), int(match2.group(1))))
                    data[match1.group(1)].append({'color': match2.group(2), 'num': int(match2.group(1))})
    logging.debug("{0}".format(data))

    print("Part 1: %d" % (count_part1(data, 'shiny gold')))
    print("Part 2: %d" % (count_part2(data, 'shiny gold')))
