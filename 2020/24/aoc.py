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


size = 500
tiles = [[['w'] * size for i in range(size)] for j in range(size)]
cx = int(size/2)
cy = int(size/2)
cz = int(size/2)

def showtiles():
    out = ""
    for row in tiles:
        for col in row:
            out += col
        out += "\n"
    print(out)

def optimize(seq):
    #eliminate any pairs of opposites
    data = copy.copy(seq)

    logging.debug("optimize start with: {}".format(data))
    hmap = {}
    for i in range(len(seq)):
        d = seq[i]
        if d in hmap:
            hmap[d].append(i)
        else:
            hmap[d] = [i]

    for (a,b) in [('e','w'), ('ne','sw'), ('nw','se')]:
        if (a not in hmap) or (b not in hmap):
            continue
        logging.debug("{}: {}".format(a, hmap[a]))
        logging.debug("{}: {}".format(b, hmap[b]))
        for i in range(min(len(hmap[a]), len(hmap[b]))):
            logging.debug("i: {} remove {} and {}".format(i, a, b))
            data.remove(a)
            data.remove(b)
        logging.debug("{}".format(data))

    return data

def flip(tile):
    x = cx
    y = cy
    z = cz

    logging.debug("flip: {}".format(tile))
    logging.debug(" {}: [{},{},{}]".format('begin', x, y, z))
    for step in tile:
        if step == 'e':
            x += 1
            y -= 1
        elif step == 'w':
            x -= 1
            y += 1
        elif step == 'se':
            y -= 1
            z += 1
        elif step == 'nw':
            y += 1
            z -= 1
        elif step == 'sw':
            x -= 1
            z += 1
        elif step == 'ne':
            x += 1
            z -= 1
        else:
            logging.error("Unknown step: {}".format(step))

        logging.debug(" {}: [{},{},{}]".format(step, x, y, z))

    if (x >= size) or (y >= size) or (z >= size):
        print("size not big enough; raise to at least {}".format(max(x,y,z)))
        raise ValueError
        
    logging.debug(" flip [{},{},{}] from {}".format(x, y, z, tiles[z][y][x]))
    if tiles[z][y][x] == 'w':
        tiles[z][y][x] = 'b'
    else:
        tiles[z][y][x] = 'w'
    logging.info(" flipped [{},{},{}] to {}".format(x, y, z, tiles[z][y][x]))

def count_tiles(color):

    count = 0
    for z in tiles:
        for y in z:
            count += y.count(color)
#            for x in y:
#                count += (x == color)
    return count

def part1(data):
    for tile in data:
        flip(tile)

    return count_tiles('b')

def flip_neighbors():

    global tiles

    t = copy.deepcopy(tiles)
    for z in range(1, size-1):
        for y in range(1, size-1):
            for x in range(1, size-1):
                logging.debug("  count adj b from [{},{},{}]".format(x,y,x))
                adj_b =  tiles[z][y-1][x+1] == 'b'  # east
                adj_b += tiles[z][y+1][x-1] == 'b'  # west
                adj_b += tiles[z+1][y-1][x] == 'b'  # se
                adj_b += tiles[z-1][y+1][x] == 'b'  # nw
                adj_b += tiles[z+1][y][x-1] == 'b'  # sw
                adj_b += tiles[z-1][y][x+1] == 'b'  # ne
                logging.debug("  [{},{},{}] has {} 'b' neighbors".format(x,y,x,adj_b))
                if tiles[z][y][x] == 'b':
                    if adj_b == 0 or adj_b > 2:
                        logging.debug("  [{},{},{}] flipping from 'b' to 'w'".format(x,y,x))
                        t[z][y][x] = 'w'
                        if (min(x,y,z) <= 1) or (max(x,y,z) >= size-2):
                            print("Error: got to the edge")
                            raise ValueError
                else:
                    if adj_b == 2:
                        logging.debug("  [{},{},{}] flipping from 'w' to 'b'".format(x,y,x))
                        t[z][y][x] = 'b'
                        if (min(x,y,z) == 0) or (max(x,y,z) == size-1):
                            print("Error: got to the edge")
                            raise ValueError
    tiles = t

def part2():

    for day in range(1, 101):
        flip_neighbors()
        logging.info("Day {}: {}".format(day, count_tiles('b')))

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []

    for line in fileinput.input():
        linedata = []
        i = 0
        while( i < len(line.rstrip())):
            if line[i] == 'n' or line[i] == 's':
                linedata.append(line[i:i+2])
                i += 2
            else:
                linedata.append(line[i:i+1])
                i += 1
        data.append(optimize(linedata))
#        data.append(linedata)

    logging.debug("Data: {}".format(data))
   
    result = part1(data)
    print("Part1: {}".format(result))

    result = part2()
    print("Part2: {}".format(result))
