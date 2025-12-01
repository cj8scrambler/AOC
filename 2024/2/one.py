#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def part1(data):
  result = 0

  for n,report in enumerate(data):
    print(f"record-{n}: {report}")
    direction = 0
    invalid = False;
    last = report[0]
    for data in report[1:]:
      if direction == 0:
        #print(f"direction not set for report-{n}")
        if (data > last):
          direction = 1 # positive
          #print(f"report-{n} should ascend; direction = {direction}")
        elif (data < last):
          direction = -1 # negative
          #print(f"report-{n} should descend; direction = {direction}")
        else:
          print(f"report-{n} no change: [0]={last}  [1]={data}")
          invalid = True;
          break # equal is invalid

      delta = data - last
      #print(f"report-{n} on {data}; delta={delta}")

      if (direction > 0) and (delta not in [1, 2, 3]):
          print(f"report-{n} invalid because '{data}' not ascending safely (delta: {delta})")
          invalid = True;
          break

      if (direction < 0) and (delta not in [-1, -2, -3]):
          print(f"report-{n} invalid because '{data}' not decending safely (delta: {delta})")
          invalid = True;
          break
      last = data

    if not invalid:
      result += 1
      print(f"report-{n} valid (direction: {direction}) (result: {result})")
    
  return(result)

def part2(data):
  result = 0

  for n,report in enumerate(data):
    invalid = 0;

    while (invalid < 2):

      direction = 0
      restart = False
      last = report[0]
      print("")
      print(f"record-{n}: {report}")

      for i,data in enumerate(report[1:]):
        if direction == 0:
          #print(f"direction not set for report-{n}")
          if (data > last):
            direction = 1 # positive
            #print(f"report-{n} should ascend; direction = {direction}")
          elif (data < last):
            direction = -1 # negative
            #print(f"report-{n} should descend; direction = {direction}")
          else:
            report.pop(i+1)
            invalid += 1
            restart = True
#            print(f"report-{n} restart: no change: [0]={last}  [1]={data}")
            break

        if (direction != 0):
          delta = data - last
          #print(f"report-{n} on {data}; delta={delta}")

          if (direction > 0) and (delta not in [1, 2, 3]):
            if (i == 1) and ((report[3] - data) < 0):
              report.pop(0)
#              print(f"report-{n} SPECIAL CASE: bad because '{data}' not ascending safely (delta: {delta}) but direction looks wrong")
            else:
              report.pop(i+1)
#              print(f"report-{n} restart: bad because '{data}' not ascending safely (delta: {delta})")
            invalid += 1
            restart = True
            break

          if (direction < 0) and (delta not in [-1, -2, -3]):
            if (i == 1) and ((report[3] - data) > 0):
              report.pop(0)
#              print(f"report-{n} SPECIAL CASE: bad because '{data}' not decending safely (delta: {delta}) but direction looks wrong")
            else:
#              print(f"report-{n} restart: bad because '{data}' not decending safely (delta: {delta})")
              report.pop(i+1)
            invalid += 1
            restart = True
            break

          #print(f"  data[{i+1}] '{data}' seems good")
          last = data

      if not restart and invalid <= 1:
        result += 1
        print(f"report-{n} valid (direction: {direction}) (result: {result})")
        invalid = 10 # just to get out of the while loop

  return(result)
  

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [[int(i) for i in line.strip().split()] for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))
