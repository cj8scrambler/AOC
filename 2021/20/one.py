#!/usr/bin/python

import logging
import sys
import fileinput
import csv
import time
from functools import reduce

CARD_SIZE=5
current_v = None
  
def check_winner():
    for c in cards.keys():
        if cards[c] is None:
            continue
        logging.info("DZ: look for winner in card-{}: {}".format(c, cards[c]))
        column = [0] * CARD_SIZE
        for y in range(CARD_SIZE):
            # Look for a row win
            if all(i < 0 for i in cards[c][y]):
                logging.info("Found win card-{} row-{}: {}".format(c, y, cards[c][y]))
                return c

            # Look for a column win
            # Count the negatives in each column
            for x in range(CARD_SIZE):
                if cards[c][y][x] < 0:
                    column[x] += 1
        logging.debug("  card-{} column-{} counts: {}".format(c, x, column))
        if CARD_SIZE in column:
            i = column.index(5)
            logging.info("Found win card-{} column-{}: {}".format(c, i, [y[i] for y in cards[c]]))
            return c
    logging.debug("No winner yet")
    return None

def bingo(values, cards):
    global current_v
    # First see if there are any leftover winners
    winner = check_winner();
    if winner is not None:
        sum = 0
        logging.info("found a winner on card-{}".format(winner))
        for y in range(CARD_SIZE):
            for x in range(CARD_SIZE):
                if cards[winner][y][x] >= 0:
                    sum += cards[winner][y][x]
                    logging.debug("  add cards[{}][{}][{}]: {}  sum: {}".format(winner,y,x,cards[winner][y][x], sum))
        logging.info("sum: {}  val: {}  product: {}".format(sum, current_v, sum*current_v))
        cards[winner] = None
        return ((winner, sum*current_v))
    while values:
        current_v = values.pop(0)
        logging.info("Playing value: {}".format(current_v))
        for c in cards.keys():
            if cards[c] is None:
                continue
            for y in range(CARD_SIZE):
                for x in range(CARD_SIZE):
                    if current_v == cards[c][y][x]:
                        logging.debug("  Found match on card-{} y-{} x-{} for value {}".format(c, y, x, current_v))
                        #special case since this doesn't work for 0:
                        if cards[c][y][x] == 0:
                            cards[c][y][x] = -0.0001
                        else:
                            cards[c][y][x] *= -1
        winner = check_winner();
        if winner is not None:
            sum = 0
            logging.info("found a winner on card-{}".format(winner))
            for y in range(CARD_SIZE):
                for x in range(CARD_SIZE):
                    if cards[winner][y][x] >= 0:
                        sum += cards[winner][y][x]
                        logging.debug("  add cards[{}][{}][{}]: {}  sum: {}".format(winner,y,x,cards[winner][y][x], sum))
            logging.info("sum: {}  val: {}  product: {}".format(sum, current_v, sum*current_v))
            cards[winner] = None
            return ((winner, sum*current_v))
    logging.debug("No winner found")
    return((None, None))

def pdata(data):

    out = '\n'
    for y,row in enumerate(data):
        for x,val in enumerate(row):
            if data[y][x]:
                out += data[y][x]
            else:
                out += ' '
        out += '\n'
    return out

def part1(data, algo, steps):

    for s in range(steps):
        # expand by 2 '.' in each direction
        newdata = [['.'] * (len(data[0]) + 4)]
        newdata.append(['.'] * (len(data[0]) + 4))
        for y,row in enumerate(data):
            newdata.append(['.'] * 2 + [i for i in row] + ['.'] * 2)
        newdata.append(['.'] * (len(data[0]) + 4))
        newdata.append(['.'] * (len(data[0]) + 4))

        data = [ ['.'] * len(newdata[0]) for _ in range(len(newdata))]

        logging.debug("newdata:")
        logging.debug(pdata(newdata))

        for y in range(1, len(newdata) - 1):
            for x in range(1, len(newdata[0])-1):
                vstr = ''
                for neighbor in [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y,x), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)]:
                    logging.debug("({},{}) neighbor {}: {}".format(y,x,neighbor,newdata[neighbor[0]][neighbor[1]]))
                    if newdata[neighbor[0]][neighbor[1]] == '.':
                        vstr += '0'
                    else:
                        vstr += '1'
                value = int(vstr, 2)
                logging.debug(" ({},{}): {} ({}) -> {}".format(y,x, value, vstr, algo[value]))
                data[y][x] = algo[value]
        logging.info("result:")
        logging.info(pdata(data))

        points = 0
        for y,row in enumerate(data):
            for x,val in enumerate(row):
                if val == '#':
                    points += 1
        logging.debug("{} points set".format(points))

    return points


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    inp = fileinput.input()
    algo = [ i for i in next(inp).rstrip() ]
    logging.debug("algo: {}".format(algo))

    data = []
    for line in inp:
        if len(line.rstrip()):
            data.append([ i for i in line.rstrip()])
    logging.debug("data: {}".format(data))


    before = time.time()
    result = part1(data, algo, 2)
    after = time.time()
    print("part 1 result: {}".format(result))
