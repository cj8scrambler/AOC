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
        
def allergens(data):

    solution = {}
    while (len(solution) != len(data)):
        for a in data.keys():
            #logging.debug("On allergen: {}".format(a))
            if (len(data[a]['possible']) == 1):
                solution[a] = data[a]['possible'].pop()
                for b in data.keys():
                    try:
                        #logging.debug("    remove {} from {} list".format(solution[a],b))
                        data[b]['possible'].remove(solution[a])
                    except KeyError:
                        pass
    #logging.debug("solution ({}): {}".format(len(solution), solution))
    return solution


def part1(data, all_i):

    i = set()
    for each in data.keys():
        for j in data[each]['all']:
            i = i | set(j)

    logging.debug("all ingredients: {}".format(all_i))
    logging.debug("set ingredients: {}".format(i))

    for a in allergens(data).values():
        i.remove(a)

    logging.debug("safe ingredients: {}".format(i))
    count = 0
    for s in i:
        #logging.debug("%s occurs %d times" % (s, all_i.count(s)))
        count += all_i.count(s)

    return count

def part2(data):

    a = allergens(data)
    logging.debug("allergens: {}".format(a))

    print("Part2 solution: ")
    for key in sorted(a.keys()):
        print("{},".format(a[key]), end='')
    print("")

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    tilepat = re.compile(r"^Tile ([\d]+):")

    data = {}
    all_i = []

    for line in fileinput.input():
        in_alg = False
        ing = []
        alg = []
        for word in line.rstrip().split():
            if '(' in word:
                in_alg = True
            else:
                if in_alg:
                    alg.append(word.strip(',').strip(')'))
                else:
                    ing.append(word)
        #logging.debug("Alg: {}  Ing: {}".format(alg,ing))
        for a in alg:
            if a in data:
                data[a]['all'].append(ing)
                data[a]['possible'] = data[a]['possible'] & set(ing)
            else:
                data[a] = {'possible': set(ing), 'all': [ing]}
        for i in ing:
            all_i.append(i)

    logging.debug("Data: {}".format(data))

    #result = part1(data, all_i)
    #print("Part1: %d" % result)
    result = part2(data)
