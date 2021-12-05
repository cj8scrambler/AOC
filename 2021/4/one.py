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

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    cards = {}
    card = 0
    y=0

    inp = fileinput.input()
    values = [int(i) for i in inp.next().rstrip().split(',')]
    logging.debug("values: {}".format(values))

    for line in inp:
        if (len(line.strip()) == 0):
            continue
        if card not in cards:
            cards[card] = [ [], [], [], [], [] ]
        cards[card][y] = [int(i) for i in line.split()]
        y += 1
        if (y == CARD_SIZE):
            logging.debug("Created card-{}: {}".format(card, cards[card]))
            y = 0
            card += 1

    cardscores = []

    before = time.time()
    cardscores.append( bingo(values, cards) )
    after = time.time()
    print("part 1 winning card: {} score: {} ({:.3f} sec)".format(cardscores[0][0], cardscores[0][1], after - before))

    while (cardscores[-1][0] != None):
        cardscores.append( bingo(values, cards) )
        print("  next winning card: {} score: {}".format(cardscores[-1][0], cardscores[-1][1]))
