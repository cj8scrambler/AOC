#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import statistics
import copy
import math
import binascii
from heapq import heappush, heappop
from collections import deque
from collections import Counter
from functools import reduce

def pdata(loc, target):

    top = max(list(target['y']) + [loc[1]])
    bot = min(list(target['y']) + [loc[1]])

    out = "\n"
    #for y in range(abs(ydelta) + 1):
    for y in range(top, bot-1, -1):
        for x in range(target['x'][1] + 1):
            if loc == (x,y):
                out += "#"
            elif (x == 0) and (y == 0):
                out += "0"
            elif (x >= target['x'][0]) and (x <= target['x'][1]) and \
                 (y >= target['y'][0]) and (y <= target['y'][1]):
                out += "T"
            else:
                out += "."
        out += "\n"
    return out

def fire(loc, velocity, target):

    logging.info("{}fire(loc: {} vel: {})".format(' '*loc[0], loc, velocity))

    l_x = loc[0] + velocity[0]
    v_x = velocity[0]
    if v_x < 0:
        v_x += 1
    elif v_x > 0:
        v_x -= 1

    l_y = loc[1] + velocity[1]
    v_y = velocity[1] - 1

    logging.debug("{}  new loc: {} vel: {})".format(' '*loc[0], (l_x, l_y), (v_x, v_y)))
    logging.debug(pdata((l_x, l_y), target))

    # Check relation to target
    if l_x > target['x'][1]:
        logging.info("{}  Too far right; miss)".format(' '*l_x))
        raise EOFError("Missed")
    else:
        if l_y < min(target['y']):
            logging.info("{}  below target; miss)".format(' '*l_x))
            raise EOFError("Missed")
        elif ((l_y >= target['y'][0]) and (l_y <= target['y'][1]) and \
              (l_x >= target['x'][0]) and (l_x <= target['x'][1])):
            logging.info("{}  HIT".format(' '*l_x))
            return l_y
        # Otherwise keep going
        logging.debug("{}  Keep going)".format(' '*l_x))
        return max(l_y, fire((l_x, l_y), (v_x, v_y), target))

def part2(target):

    steps = None

    # Just do the  sweep back and forth trying to hit the target.
    #   once you find a hit, then save it to a hit queue

    #   while queue.pop():
    #     record velocty/maxy hits
    #     check all the neighbors
    #         skip any already checked
    #     add any neighbor hits to the hit queue

    #hitq = deque()
    hitq = []
    beenthere = []
    max_height=(-math.inf,(0,0))

    step = 22
    while len(hitq) == 0:
        # sweep from up->right->down in growing rings
        for v in zip( list(range(step + 1)) + list(range(step, 0, -1)), list(range(step, 0, -1)) + list(range(step + 1))):
            try:
                top = fire((0,0), v, target)
                logging.error("step-{} v: {} found a hit. top y: {}".format(step, v, top))
                beenthere.append(v)
                #hitq.append((v,top))
                heappush(hitq, (-1*top,v)) #flip height for min heap queue
                break;
            except EOFError:
                logging.info("step-{} v: {} Miss".format(step, v))
                pass
            except:
                raise
        step += 1

    R=1
    while True:

        while len(hitq):
            #v,top = hitq.popleft()
            top,v = heappop(hitq)
            top *= -1 #flip it back
            if top > max_height[0]:
                logging.error("Neighbor {} set new record: {}; go back to R=1".format(v, top))
                R=1
                max_height=(top,v)
            elif top == max_height[0]:
                logging.error("Neighbor {} matches record: {}".format(v, top))
            else:
                logging.info("Neighbor {} not a record; skip".format(v))
                continue

            # Check neighbors with (x[0:+R],y[+1])
            #for vx in range(v[0]-R, v[0]+R+1):
            #    for vy in range(v[1]+1, v[1]+3):
            # Check neighbors in radius R where ranges:
            #   X: x-R to x+R   Y: y+1 to y+R
            for vx in range(v[0]-R, v[0]+R+1):
                for vy in range(v[1]+1, v[1]+R+1):
                    if (vx,vy) not in beenthere:
                        beenthere.append((vx,vy))
                        try:
                            newtop = fire((0,0), (vx,vy), target)
                            logging.error("Check (R={}) {} neighbor {}: hit; newtop y: {}".format(R,v,(vx,vy), newtop))
                            #hitq.append(((vx,vy),newtop))
                            heappush(hitq, (-1*newtop,(vx,vy))) #flip height for min heap queue
                        except EOFError:
                            logging.error("Check (R={}) {} neighbor {}: miss".format(R, v,(vx,vy)))
                            pass
                        except:
                            raise
                    else:
                        logging.info("Check {} neighbor {}: already been there".format(v,(vx,vy)))

        logging.error("Finished checking R={}.  Go back to last record: {} (top {})".format(R, max_height[1], max_height[0]))
        # Push the last known element back and expand the search
        heappush(hitq, (-1*max_height[0],max_height[1])) #flip height for min heap queue
        R += 1


def part1(target):

    steps = None


#    # Initial testing of examples
#    for v in [(7,2), (6,3), (9,0), (17,-4)]:
#        try:
#            topy = fire((0,0), v, target)
#            logging.error("{}: hit with top y: {}".format(v, topy))
#        except EOFError:
#            logging.error("{}: Miss".format(v))
#        except:
#            raise

    # Actual part 1 solution:
    #   sweep back and forth trying to hit the target.
    #   once you find a hit, then save it to a hit queue

    #   while queue.pop():
    #     record velocty/maxy hits
    #     check all the neighbors
    #         skip any already checked
    #     add any neighbor hits to the hit queue

    #hitq = deque()
    hitq = []
    beenthere = []
    max_height=(-math.inf,(0,0))

    step = 22
    while len(hitq) == 0:
        # sweep from up->right->down in growing rings
        for v in zip( list(range(step + 1)) + list(range(step, 0, -1)), list(range(step, 0, -1)) + list(range(step + 1))):
            try:
                top = fire((0,0), v, target)
                logging.error("step-{} v: {} found a hit. top y: {}".format(step, v, top))
                beenthere.append(v)
                #hitq.append((v,top))
                heappush(hitq, (-1*top,v)) #flip height for min heap queue
                break;
            except EOFError:
                logging.info("step-{} v: {} Miss".format(step, v))
                pass
            except:
                raise
        step += 1

    R=1
    while True:

        while len(hitq):
            #v,top = hitq.popleft()
            top,v = heappop(hitq)
            top *= -1 #flip it back
            if top > max_height[0]:
                logging.error("Neighbor {} set new record: {}; go back to R=1".format(v, top))
                R=1
                max_height=(top,v)
            elif top == max_height[0]:
                logging.error("Neighbor {} matches record: {}".format(v, top))
            else:
                logging.info("Neighbor {} not a record; skip".format(v))
                continue

            # Check neighbors with (x[0:+R],y[+1])
            #for vx in range(v[0]-R, v[0]+R+1):
            #    for vy in range(v[1]+1, v[1]+3):
            # Check neighbors in radius R where ranges:
            #   X: x-R to x+R   Y: y+1 to y+R
            for vx in range(v[0]-R, v[0]+R+1):
                for vy in range(v[1]+1, v[1]+R+1):
                    if (vx,vy) not in beenthere:
                        beenthere.append((vx,vy))
                        try:
                            newtop = fire((0,0), (vx,vy), target)
                            logging.error("Check (R={}) {} neighbor {}: hit; newtop y: {}".format(R,v,(vx,vy), newtop))
                            #hitq.append(((vx,vy),newtop))
                            heappush(hitq, (-1*newtop,(vx,vy))) #flip height for min heap queue
                        except EOFError:
                            logging.error("Check (R={}) {} neighbor {}: miss".format(R, v,(vx,vy)))
                            pass
                        except:
                            raise
                    else:
                        logging.info("Check {} neighbor {}: already been there".format(v,(vx,vy)))

        logging.error("Finished checking R={}.  Go back to last record: {} (top {})".format(R, max_height[1], max_height[0]))
        # Push the last known element back and expand the search
        heappush(hitq, (-1*max_height[0],max_height[1])) #flip height for min heap queue
        R += 1

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    target = {}
    for line in fileinput.input():
        #target area: x=20..30, y=-10..-5
        g = re.match( r"^target area: x=(-?\d+)..(-?\d+).*y=(-?\d+)\.\.(-?\d+)", line)
        if g:
            txmin, txmax, tymin, tymax = int(g.group(1)), int(g.group(2)), int(g.group(3)), int(g.group(4))
            target = {'x': (txmin, txmax), 'y': (tymin, tymax)}

    logging.debug('target: {}'.format(target))

    before = time.time()
    result = part1(target)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    (result,length) = handle_packet(data)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))
