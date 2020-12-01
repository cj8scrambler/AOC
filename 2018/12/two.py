#!/usr/bin/python3

import sys
import re
import numpy as np

LBUF=1
RBUF=1

graph = dict()
last_state = []
next_state = []
rules = []

def print_gen(gen):
    ''' negative generation means print the header instead '''
    if gen < 0:
        print("    ", end="")
        i = -1 * (LBUF)
        while (i < (len(last_state) - LBUF)):
            if (i >= 0) and ((i % 10) == 0):
                print("%1d" % int(i/10), end="")
            else:
                print(" ", end="")
            i = i+1
        print ("");
        print ("    ", end="");
        i = -1 * (LBUF)
        while (i < (len(last_state) - LBUF)):
            if (i >= 0) and ((i % 10) == 0):
                print("0", end="")
            else:
                print(" ", end="")
            i = i+1
        print ("");
    else:
        print("%2d: " % (gen), end="")
        i = -1 * (LBUF)
        while (i < (len(last_state) - LBUF)):
            print("%c" % (last_state[i+LBUF]), end="")
            i = i+1
    print("")
    

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        if 'initial state:' in source:
            last_state =  ['.'] * LBUF + list(source.replace('initial state: ','').rstrip()) + ['.'] * RBUF
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
newheader = 0
print_gen(generation)

while (generation < int(sys.argv[2])):
#    if (newheader):
#        print_gen(-1)
    next_state = ['.'] * len(last_state)
    plant = -1 * LBUF
    while ((plant) < len(last_state) - LBUF):
        rulenum = 0
        match = 0
        while ((rulenum) < len(rules)):
            if (rules[rulenum]['condition'] == last_state[plant+LBUF-2:plant+LBUF+3]):
                next_state[plant+LBUF] = rules[rulenum]['result'][0];
#                print ("  got a match; set plant-%d=%s; next_state: %s" % (plant, rules[rulenum]['result'], next_state))
                match = 1
            rulenum += 1
#        if (not match):
#            print ("  no match")




        plant += 1

    newheader=0
    if ('#' in next_state[:3]):
#        print ("WARNING: generation-%d: plants getting close to left boundary" % (generation+1))
        LBUF+=1
        next_state.insert(0,'.')
        newheader=1
    elif (['.'] * 4 == next_state[:4]):
#        print ("WARNING: generation-%d: extra space on left boundary" % (generation+1))
        LBUF-=1
        del next_state[0]
        newheader=1

    if ('#' in next_state[-3:]):
#        print ("WARNING: generation-%d: plants getting close to right boundary" % (generation+1))
        RBUF+=1
        next_state.append('.')
    elif (['.'] * 4 == next_state[-4:]):
#        print ("WARNING: generation-%d: extra space on right boundary" % (generation+1))
        RBUF-=1
        del next_state[len(next_state)-1]

    generation += 1
    last_state = next_state

    if (generation % 1000) == 0:
        sum = 0
        i = 0
        while (i < len(last_state)):
            plant = i - LBUF
            if last_state[i] is '#':
                sum += plant
            i += 1

        print("RBUF=%d  LBUF=%d" % (LBUF, RBUF))
        print("Generation-%d total: %d" % (generation, sum))
        print_gen(-1)
        print_gen(generation)
        print("");
#    print ("  end of gen-%d; last_state now: %s" %(generation, last_state))

sum = 0
i = 0
while (i < len(last_state)):
    plant = i - LBUF
    if last_state[i] is '#':
        sum += plant
    i += 1

print("Finished with RBUF=%d  LBUF=%d" % (LBUF, RBUF))
print("Generation-%d total: %d" % (generation, sum))
