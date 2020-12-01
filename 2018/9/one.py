#!/usr/bin/python3

from itertools import cycle
import sys
import re

players = int(sys.argv[1])
marbles = int(sys.argv[2])
scores = dict()

data = [0]
cur = 0
player = 1
marble = 1

print("Players: %d\nMarbles: %d" % (players, marbles))

def inc(val):
    val += 1
    if (val == len(data)):
        val = 0;
    return val

def dec(val):
    if (val == 0):
        val = len(data) - 1;
    else:
        val -= 1
    return val

while marble <= marbles:
    if (marble % 1000) == 0:
        print("Player-%03d Marble-%08d" % (player, marble))
    if ((marble % 23) == 0):
        cur = dec(cur);
        cur = dec(cur);
        cur = dec(cur);
        cur = dec(cur);
        cur = dec(cur);
        cur = dec(cur);
        cur = dec(cur);
        scores[player] = scores.get(player,0) + marble + data[cur]
        #print("Player %d: Marble #%d: special case: remove %d  score: %d" % (player, marble, data[cur], marble + data[cur]))
        del data[cur]
    else:
        cur = inc(cur);
        data.insert(cur+1, marble) # not wrapping is actually good here; changes 'insert' to an 'append' action
        cur = inc(cur);
        #print("Player %d: %s" % (player, data))

    player += 1
    if (player > players):
        player = 1
    marble += 1

print ("Total board size: %d" % (len(data)))
top = list(scores.keys())[0]
for each in scores.keys():
    if (scores[each] > scores[top]):
        top = each
print ("Top score: Player-%d: %d" % (top, scores[top]))
