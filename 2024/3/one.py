#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

'''
states:
  0 looking for m or d->10
  1 looking for u
  2 looking for l
  3 looking for (
  4 looking for first number
  5 looking for ,
  6 looking for second number
  7 looking for )
  8 mul success

  10 looking for o
  11 looking for ( or n->20
  12 looking for )
  13 got a do()

  20 looking for '
  21 looking for t
  22 looking for (
  23 looking for )
  24 got a don't()
'''

def part2(data):
  result = 0
  do = True

  for line in data:
    i=0
    state=0
    print(f"line: {line}")

    while i < len(line):
      if state == 0:
        d1=""
        d2=""
        print(f"i: {i} state={state} on: {line[i]}")
        if line[i] == 'm':
          state += 1
          print(f"i: {i} found m; state: {state}")
        elif line[i] == 'd':
          state =10
          print(f"i: {i} found d; state: {state}")
        else:
          state = 0
      elif state == 1:
        if line[i] == 'u':
          state += 1
          print(f"i: {i} found u; state: {state}")
        else:
          state = 0
      elif state == 2:
        if line[i] == 'l':
          state += 1
          print(f"i: {i} found l; state: {state}")
        else:
          state = 0
      elif state == 3:
        if line[i] == '(':
          state += 1
          print(f"i: {i} found (; state: {state}")
        else:
          state = 0
      elif state == 4:
        if line[i].isdigit():
          d1 += line[i]
          if (len(d1) == 3):
            print(f"i: {i} full num, d1: {d1}; state: {state}")
            state += 1
        elif line[i] == ',':
          state += 2
          print(f"i: {i} found , d1: {d1}; state: {state}")
        else:
          state = 0
      elif state == 5:
        if line[i] == ',':
          state += 1
          print(f"i: {i} found ,; state: {state}")
        else:
          state = 0
      elif state == 6:
        print(f"  state=6: checking on {line[i]}")
        if line[i].isdigit():
          d2 += line[i]
          if (len(d2) == 3):
            print(f"i: {i} full num, d2: {d2}; state: {state}")
            state += 1
        elif line[i] == ')':
          state += 2
          print(f"i: {i} found , d2: {d2}; state: {state}")
        else:
          state = 0
      elif state == 7:
        if line[i] == ')':
          state += 1
          print(f"i: {i} found ); state: {state}")
        else:
          state = 0
      elif state == 10:
        if line[i] == 'o':
          state += 1
          print(f"i: {i} found o; state: {state}")
        else:
          state = 0
      elif state == 11:
        if line[i] == '(':
          state += 1
          print(f"i: {i} found (; state: {state}")
        elif line[i] == 'n':
          state = 20
          print(f"i: {i} found n; state: {state}")
        else:
          state = 0
      elif state == 12:
        if line[i] == ')':
          state += 1
          print(f"i: {i} found ); got a do() state: {state}")
        else:
          state = 0
      elif state == 20:
        if line[i] == "'":
          state += 1
          print(f"i: {i} found '; state: {state}")
        else:
          state = 0
      elif state == 21:
        if line[i] == "t":
          state += 1
          print(f"i: {i} found t; state: {state}")
        else:
          state = 0
      elif state == 22:
        if line[i] == "(":
          state += 1
          print(f"i: {i} found (; state: {state}")
        else:
          state = 0
      elif state == 23:
        if line[i] == ")":
          state += 1
          print(f"i: {i} found ); got a don't() state: {state}")
        else:
          state = 0

      if state == 8:
        if do:
          result += int(d1) * int(d2)
          print(f"i: {i} state: {state}  {int(d1)} x {int(d2)} = {int(d1) * int(d2)}  result: {result}")
        else:
          print(f"i: {i} state: {state}  SKIP the MUL")
        state = 0
      elif state == 13:
        do = True
        state = 0
        print(f"i: {i} handle do(); state: {state}")
      elif state == 24:
        do = False
        state = 0
        print(f"i: {i} handle don't(); state: {state}")

      i += 1

  return(result)

'''
states:
  0 looking for m
  1 looking for u
  2 looking for l
  3 looking for (
  4 looking for first number
  5 looking for ,
  6 looking for second number
  7 looking for )
  8 success
'''

def part1(data):
  result = 0

  for line in data:
    i=0
    state=0
    print(f"line: {line}")

    while i < len(line):
      if state == 0:
        d1=""
        d2=""
        print(f"i: {i} state={state} on: {line[i]}")
        if line[i] == 'm':
          state += 1
          print(f"i: {i} found m; state: {state}")
        else:
          state = 0
      elif state == 1:
        if line[i] == 'u':
          state += 1
          print(f"i: {i} found u; state: {state}")
        else:
          state = 0
      elif state == 2:
        if line[i] == 'l':
          state += 1
          print(f"i: {i} found l; state: {state}")
        else:
          state = 0
      elif state == 3:
        if line[i] == '(':
          state += 1
          print(f"i: {i} found (; state: {state}")
        else:
          state = 0
      elif state == 4:
        if line[i].isdigit():
          d1 += line[i]
          if (len(d1) == 3):
            print(f"i: {i} full num, d1: {d1}; state: {state}")
            state += 1
        elif line[i] == ',':
          state += 2
          print(f"i: {i} found , d1: {d1}; state: {state}")
        else:
          state = 0
      elif state == 5:
        if line[i] == ',':
          state += 1
          print(f"i: {i} found ,; state: {state}")
        else:
          state = 0
      elif state == 6:
        print(f"  state=6: checking on {line[i]}")
        if line[i].isdigit():
          d2 += line[i]
          if (len(d2) == 3):
            print(f"i: {i} full num, d2: {d2}; state: {state}")
            state += 1
        elif line[i] == ')':
          state += 2
          print(f"i: {i} found , d2: {d2}; state: {state}")
        else:
          state = 0
      elif state == 7:
        if line[i] == ')':
          state += 1
          print(f"i: {i} found ); state: {state}")
        else:
          state = 0

      if state == 8:
        result += int(d1) * int(d2)
        print(f"i: {i} state: {state}  {int(d1)} x {int(d2)} = {int(d1) * int(d2)}  result: {result}")
        state = 0


      i += 1

  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [l for l in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))
