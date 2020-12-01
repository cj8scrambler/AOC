#!/usr/bin/python

import sys
import fileinput

i = 0
sum = 0

def calc_fuel(mass):
    result = int(mass / 3) - 2
#    print ("  mass: %d  result: %d" % (mass, result))
    if (result < 0):
#        print ("  Returning 0")
        return 0
#    print ("  Recursing")
    return (result + calc_fuel(result))

with open(sys.argv[1], 'r') as data:
    for line in data:
        mass = int(line)
#        print ("i: %d  mass: %d  value: %s" % (i, mass, line))
        fuel = calc_fuel(mass)
        sum += fuel
        print ("i: %d mass: %d  fuel: %d  sum: %d" % (i, mass, fuel, sum))
        i += 1

print("Sum: %d" % (sum))
