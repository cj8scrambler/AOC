#!/usr/bin/python3

import sys
import re
import numpy as np

SHIFT=20

graph = dict()
last_state = []
next_state = []
rules = []

def print_gen(gen):
    ''' negative generation means print the header instead '''
    if gen < 0:
        print("    ", end="")
        i = -1 * (SHIFT)
        while (i < (len(last_state) - SHIFT)):
            if (i >= 0) and ((i % 10) == 0):
                print("%1d" % int(i/10), end="")
            else:
                print(" ", end="")
            i = i+1
        print ("");
        print ("    ", end="");
        i = -1 * (SHIFT)
        while (i < (len(last_state) - SHIFT)):
            if (i >= 0) and ((i % 10) == 0):
                print("0", end="")
            else:
                print(" ", end="")
            i = i+1
        print ("");
    else:
        print("%2d: " % (gen), end="")
        i = -1 * (SHIFT)
        while (i < (len(last_state) - SHIFT)):
            print("%c" % (last_state[i+SHIFT]), end="")
            i = i+1
    print("")
    

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        if 'initial state:' in source:
            last_state =  ['.'] * SHIFT + list(source.replace('initial state: ','').rstrip()) + ['.'] * SHIFT
        if '=>' in source:
            rules.append({'condition' : list(source)[0:5], 'result' : list(source)[9]})
    print ("Initiial state: %s" % (last_state))

    i = 0
    while i < len(rules):
        print ("Rule-%d: %s -> %s" % (i, rules[i]['condition'], rules[i]['result']))
        i += 1
   
print("")
print_gen(-1)
generation = 0
print_gen(generation)

while (generation < int(sys.argv[2])):
    next_state = ['.'] * len(last_state)
    plant = int(SHIFT/-2)
    while ((plant) < len(last_state) - SHIFT):
        rulenum = 0
        match = 0
        while ((rulenum) < len(rules)):
#            print ("  plant-%d: Before: %s  Rule-%d: %s -> %s" % (plant, last_state[plant+SHIFT-2:plant+SHIFT+3], rulenum, rules[rulenum]['condition'], rules[rulenum]['result']))
            if (rules[rulenum]['condition'] == last_state[plant+SHIFT-2:plant+SHIFT+3]):
                next_state[plant+SHIFT] = rules[rulenum]['result'][0];
#                print ("  got a match; set plant-%d=%s; next_state: %s" % (plant, rules[rulenum]['result'], next_state))
                match = 1
            rulenum += 1
#        if (not match):
#            print ("  no match")




        plant += 1

    if ('#' in next_state[:3]):
        print ("WARNING: generation-%d: plants getting close to left boundary" % (generation+1))
    if ('#' in next_state[-3:]):
        print ("WARNING: generation-%d: plants getting close to right boundary" % (generation+1))

    generation += 1
    last_state = next_state
    print_gen(generation)
#    print ("  end of gen-%d; last_state now: %s" %(generation, last_state))

sum = 0
i = 0
while (i < len(last_state)):
    plant = i - SHIFT
    if last_state[i] is '#':
        sum += plant
    i += 1

print("Generation-%d total: %d" % (generation, sum))
