#!/usr/bin/env python3

import logging
import sys
import fileinput
import csv
import queue
import threading
import time
from itertools import permutations

def day7_part2(memory, indata, outdata):

    print("DZ:   Begin thread-%d" % (memory))
    time.sleep(memory)
    print("DZ:   Done thread-%d" % (memory))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    best_thrust=0
    atnum = 0
    threads = [None] * 5 
    #for attempt in permutations(range(5), 5):
    for attempt in [[0, 1, 2, 3, 4]]:
        atnum += 1
        print("Attempt-%d: %s" % (atnum, attempt))
        q = [queue.Queue() for i in range(len(attempt) + 1) ]

        qnum = 0
        q[qnum].put(0)
        for each in q:
            print("DZ: Done: Q size: %d" % (each.qsize()))
        for step in attempt:
            print("DZ: starting thread-%d" % (step))
            threads[qnum] = threading.Thread(target=day7_part2, args=(step, q[qnum], q[qnum+1]))
            threads[qnum].start()
            qnum += 1
        print("DZ: Done spawinging; now waiting")
        for t in threads:
            t.join()

        for each in q:
            print("DZ: Done: Q size: %d" % (each.qsize()))
