#!/usr/bin/python

import logging
import sys
import fileinput
import csv
import time
import re
from functools import reduce


SIZE=10

def part1(data):

def part1(data):

    winner = None
    score = [0,0]
    dice = 1

    while winner is None:
        for player in [0,1]:
            #logging.debug("Player-{}: start at {}".format(player, data[player]))
            for roll in range(3):
                #logging.debug("Player-{}: moves {} more spaces".format(player, dice))
                data[player] += dice
                dice += 1
            while data[player] > 10:
                data[player] -= 10 
            #logging.debug("Player-{}: ends up at space {}".format(player, data[player]))
            score[player] += data[player]
            logging.debug("Player-{}: score: {}".format(player, score[player]))
            if score[player] >= 1000:
                logging.debug("Player-{}: wins with score: {}".format(player, score[player]))
                winner = player
                break;

    looser = int(not winner)
    logging.debug("Player-{}: wins with score: {} (dice {})".format(winner, score[winner], dice))
    logging.debug("Player-{}: looses with score: {}".format(looser, score[looser]))
    return (score[looser] * (dice - 1))
            

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    pos=[]
    for line in fileinput.input():
        #Player 1 starting position: 4
        g = re.match( r"^Player .* starting position: (\d+)", line)
        if g:
            pos.append(int(g.group(1)))

    logging.debug("pos: {}".format(pos))


    before = time.time()
    result = part1(pos)
    after = time.time()
    print("part 1 result: {}".format(result))
