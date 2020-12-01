#!/usr/bin/python

import sys
import fileinput

i = 0
sum = 0

with open(sys.argv[1], 'r') as data:
    for mass in data:
        fuel = int(int(mass) / 3) - 2
        sum += fuel
        print ("i: %d mass: %d  fuel: %d  sum: %d" % (i, int(mass), fuel, sum))
        i += 1

print("Sum: %d" % (sum))
