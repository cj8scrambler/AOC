#!/usr/bin/python

import logging
import sys
import fileinput
import time
import copy
from itertools import combinations 
  
def occupied_line(data, row, seat):

    count = 0
    logging.debug("  Count line of site seats to [%d,%d]" % (row, seat))
    for irow in [-1, 0, 1]:
        for iseat in [-1, 0, 1]:
            # itterate [0,0] wouldn't go anywhere
            if (irow == 0) and (iseat == 0):
                continue
            logging.debug("   Check directions [%d, %d]" % (irow, iseat))
            lrow = row
            lseat = seat
            while (lrow >= 0) and (lrow < len(data)) and \
                  (lseat >= 0) and (lseat < len(data[lrow])):
                # skip the seat in question
                if not ((lseat == seat) and (lrow==row)):
                    if (data[lrow][lseat] == '#'):
                        count += 1
                        logging.debug("     [%d,%d] Found # (count=%d)" % (lrow, lseat, count))
                        break;
                    elif (data[lrow][lseat] == 'L'):
                        logging.debug("     [%d,%d] Found L; break" % (lrow, lseat))
                        break;

                lseat += iseat
                lrow += irow

    logging.debug("seat [%d,%d] has %d line of site adjacent" % (row, seat, count))
    return count

def occupied_adjacent(data, row, seat):

    count = 0

    logging.debug("  Count adjacent seats to [%d,%d]" % (row, seat))
    for adj_row in range(row-1, row+2):
        #skip invalid rows
        if (adj_row < 0) or (adj_row >= len(data)):
            continue
        for adj_seat in range(seat-1, seat+2):
            #skip invalid seats
            if (adj_seat < 0) or (adj_seat >= len(data[adj_row])):
                continue
            # Don't count the seat in question
            if (adj_row==row) and (adj_seat==seat):
                continue

            if (data[adj_row][adj_seat] == '#'):
                count += 1

    logging.debug("seat [%d,%d] has %d adjacent occupied" % (row, seat, count))
    return count

def wave2(data):
    for row in data:
        logging.debug("  {0}".format(row))

    newwave = copy.deepcopy(data)
    changes = 0
    for row in range(len(data)):
        for seat in range(len(data[row])):
            neighbors = occupied_line(data,row,seat)
            if (data[row][seat] == 'L') and (neighbors == 0):
                logging.debug("seat [%d,%d] becomes occupied" % (row, seat))
                newwave[row][seat] = '#'
                changes += 1
            elif (data[row][seat] == '#') and (neighbors >= 5):
                logging.debug("seat [%d,%d] becomes open" % (row, seat))
                newwave[row][seat] = 'L'
                changes += 1
            else:
                newwave[row][seat] = data[row][seat]

    return (changes, newwave)

def wave1(data):
    newwave = copy.deepcopy(data)
    changes = 0
    for row in range(len(data)):
        for seat in range(len(data[row])):
            neighbors = occupied_adjacent(data,row,seat)
            if (data[row][seat] == 'L') and (neighbors == 0):
                logging.debug("seat [%d,%d] becomes occupied" % (row, seat))
                newwave[row][seat] = '#'
                changes += 1
            elif (data[row][seat] == '#') and (neighbors >= 4):
                logging.debug("seat [%d,%d] becomes open" % (row, seat))
                newwave[row][seat] = 'L'
                changes += 1
            else:
                newwave[row][seat] = data[row][seat]

    return (changes, newwave)

def part2(data):

    changes = 1
    while (changes):
        (changes, data) = wave2(data)
        logging.info("got {0} changes".format(changes));
        for each in data:
            logging.info("{0}".format(each));

    total = 0
    for row in range(len(data)):
        total += data[row].count('#')
    logging.info("Total: {0}".format(total));

    return total

def part1(data):

    changes = 1
    while (changes):
        (changes, data) = wave1(data)
        logging.info("got {0} changes".format(changes));
        for each in data:
            logging.info("{0}".format(each));

    total = 0
    for row in range(len(data)):
        total += data[row].count('#')
    logging.info("Total: {0}".format(total));

    return total

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    data = [list(line.rstrip()) for line in fileinput.input()]

    result = part1(data)
    print("Part 1:  seats occupied: %d" % (result))

    result = part2(data)
    print("Part 2:  seats occupied: %d" % (result))
