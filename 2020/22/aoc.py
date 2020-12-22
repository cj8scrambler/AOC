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

def show(data):
    logging.info("Player {}: {}".format(1, data[1]))
    logging.info("Player {}: {}".format(2, data[2]))

def score(cards):
    mult = 1
    score = 0

    for i in range(len(cards)-1, -1, -1):
        score += cards[i] * mult
        mult += 1

    return score

def hist(cards):
    mult = 1
    score = 0

    for i in range(0, len(cards)):
        score += cards[i] * mult
        mult *= 10

    return score

def play_round_p1(data):

    # Player 1 has higher card
    if data[1][0] > data[2][0]:
        data[1].append(data[1].pop(0))
        data[1].append(data[2].pop(0))
    elif data[2][0] > data[1][0]:
        data[2].append(data[2].pop(0))
        data[2].append(data[1].pop(0))
    else:
        raise ValueError

def play_round_p2(data, gamehist, gamenum, roundnum):

    logging.error("-- Round {} (Game {}) --".format(roundnum, gamenum))
    show(data)

    logging.info("  Player 1 cards: {} ({}) hist: {}".format(data[1], hist(data[1]), gamehist[1]))
    logging.info("  Player 2 cards: {} ({}) hist: {}".format(data[2], hist(data[2]), gamehist[2]))

    # Check history
    if (hist(data[1]) in gamehist[1]):
        logging.debug("  Player 1 cards: {} ({}) was in hist: {}; Player 1 wins".format(data[2], hist(data[2]), gamehist[2]))
        return -1
    if (hist(data[2]) in gamehist[2]):
        logging.debug("  Player 2 cards: {} ({}) was in hist: {}; Player 1 wins".format(data[2], hist(data[2]), gamehist[2]))
        return -1

    # Update history
    gamehist[1].append(hist(data[1]))
    gamehist[2].append(hist(data[2]))

    # Each draw a card
    c1 = data[1].pop(0)
    c2 = data[2].pop(0)

    logging.info("  Player 1 drew {} (and has {} cards)".format(c1, len(data[1])))
    logging.info("  Player 2 drew {} (and has {} cards)".format(c2, len(data[2])))

    # Recurse if each player has enough cards
    if (len(data[1]) >= c1) and (len(data[2]) >= c2):
        recursedata = {1: data[1][0:c1], 2:data[2][0:c2]}
        logging.debug("  Both players have enough; recurse with copy: {}".format(recursedata))
        winner = part2(recursedata, gamenum + 1)
        logging.error("  subgame finished; winner: {}".format(winner))
        if winner == 1:
            data[1].append(c1)
            data[1].append(c2)
        else:
            data[2].append(c2)
            data[2].append(c1)
        return winner

    # Otherwise high card wins
    else:
        # Player 1 has higher card
        if c1 > c2:
            logging.error("    Not enough to recurse; P1 wins round")
            data[1].append(c1)
            data[1].append(c2)
            return 1
        elif c2 > c1:
            logging.error("    Not enough to recurse; P2 wins round")
            data[2].append(c2)
            data[2].append(c1)
            return 2
        else:
            raise ValueError

def part2(data, gamenum):

    r = 1
    gamehist = {1: [], 2: []}
    while (len(data[1]) > 0 and len(data[2]) > 0):
        winner = play_round_p2(data, gamehist, gamenum, r)
        if (winner < 0):
            logging.info("    P1 imediately wins subgame")
            return 1
        r += 1

    show(data)

    s = None
    if (len(data[1])):
        s = score(data[1])
        print("Player 1 won: {}".format(s))
    else:
        s = score(data[2])
        print("Player 2 won: {}".format(s))

    return winner


def part1(data):

    r = 1
    while (len(data[1]) > 0 and len(data[2]) > 0):
        logging.error("Round {}: ".format(r))
        show(data)
        play_round_p1(data)
        r += 1

    logging.error("Game Over:")
    show(data)

    s = None
    if (len(data[1])):
        s = score(data[1])
        logging.error("Player 1 won: {}".format(s))
    else:
        s = score(data[2])
        logging.error("Player 2 won: {}".format(s))

    return s

if __name__ == '__main__':

    logging.basicConfig(level=logging.CRITICAL)

    playerpat = re.compile(r"^Player ([\d]+):$")

    data = {}
    player=None

    for line in fileinput.input():
        match = playerpat.match(line)
        if match:
            player = int(match.group(1))
            data[player] = []
        else:
            try:
                data[player].append(int(line))
            except ValueError:
                logging.debug("Ignoring line: {}".format(line))

    logging.debug("Data: {}".format(data))

    #result = part1(data)
    #print("Part1: %d" % result)
    result = part2(data, 1)
