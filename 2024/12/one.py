#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
import copy
from itertools import combinations 
from collections import defaultdict 

def printmap(data):
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      print(val, end="")
    print("")

def valid(point, data):
  if (point[0] >= 0) and (point[0] < len(data[0])) and \
     (point[1] >= 0) and (point[1] < len(data)):
    return True
  return False

def cost1(points, data):
  area = len(points)
  perim = 0
  for p in points:
    perim += 4 - len(neighbors(p, data))

  return area * perim

#checks if point and neighbor indicate the line continuing
def is_line(point, neighbor, plot):
  if plot[point[1]][point[0]] == '.':
#    print(f"    isline: point: {point} is '.': return False")
    return False
  if not valid(neighbor, plot):
#    print(f"    isline: {point} is not '.' and {neighbor} is OOB: return True")
    return True
  if plot[neighbor[1]][neighbor[0]] != '.':
#    print(f"    isline: {point} is not '.' and {neighbor} is not '.': return False")
    return False
#  print(f"    isline: {point} else: return True")
  return True


def sides(points):
  #print(f"start with points: {points}")

  #Make a minimal map
  min_x = min(list(zip(*points))[0])
  max_x = max(list(zip(*points))[0])
  min_y = min(list(zip(*points))[1])
  max_y = max(list(zip(*points))[1])

  plot = [['.' for x in range(max_x-min_x+1)] for y in range(max_y-min_y+1)]
  for (x,y) in points:
    x -= min_x
    y -= min_y
    plot[y][x] = '#'

  top = 0
  bottom = 0
  for y,row in enumerate(plot):
    # Count top/bottom lines
    top_line = is_line((0,y), (0,y-1), plot)
    #print(f"Begin row-{y} with top_line={top_line}")
    bottom_line = is_line((0,y), (0,y+1), plot)
    #print(f"Begin row-{y} with bottom_line={bottom_line}")
    for x,val in enumerate(row):
      prev_top_line = top_line
      top_line = is_line((x,y), (x,y-1), plot)
      #print(f"  {(x,y)}: top_line={top_line}")
      if prev_top_line and not top_line:
          #print(f"Finished a top line at {(x,y)}")
          top += 1

      prev_bottom_line = bottom_line
      bottom_line = is_line((x,y), (x,y+1), plot)
      if prev_bottom_line and not bottom_line:
          #print(f"Finished a bottom line at {(x,y)}")
          bottom += 1
    if (top_line):
      #print(f"  end of row and top_line={top_line}: count line")
      top += 1
    if (bottom_line):
      #print(f"  end of row and bottom_line={bottom_line}: count line")
      bottom += 1

  left = 0
  right = 0
  for x,column in enumerate(zip(*plot)):
    # Count left/right lines
    left_line = is_line((x,0), (x-1,0), plot)
    #print(f"Begin row-{y} with left_line={left_line}")
    right_line = is_line((x,0), (x+1,0), plot)
    #print(f"Begin row-{y} with right_line={right_line}")
    for y,val in enumerate(column):
      prev_left_line = left_line
      left_line = is_line((x,y), (x-1,y), plot)
      #print(f"  {(x,y)}: left_line={left_line}")
      if prev_left_line and not left_line:
          #print(f"Finished a left line at {(x,y)}")
          left += 1

      prev_right_line = right_line
      right_line = is_line((x,y), (x+1,y), plot)
      if prev_right_line and not right_line:
          #print(f"Finished a right line at {(x,y)}")
          right += 1

    if (left_line):
      #print(f"  end of row and left_line={left_line}: count line")
      left += 1
    if (right_line):
      #print(f"  end of row and right_line={right_line}: count line")
      right += 1

  #printmap(plot)
  #print(f"Finished with {top} top lines; {bottom} bottom lines; {left} left lines; {right} right lines")

  return (top + bottom + left + right)

def cost2(points, data):
  area = len(points)
  num_sides = sides(points)

  #print(f"Cost: {area*num_sides}  area: {area}  sides: {num_sides}")
  return area * num_sides


def neighbors(point, data):
  result = [] 
  if valid((point[0], point[1]+1), data) and data[point[1]][point[0]] == data[point[1]+1][point[0]]:
    result.append((point[0], point[1]+1))
  if valid((point[0]+1, point[1]), data) and data[point[1]][point[0]] == data[point[1]][point[0]+1]:
    result.append((point[0]+1, point[1]))
  if valid((point[0], point[1]-1), data) and data[point[1]][point[0]] == data[point[1]-1][point[0]]:
    result.append((point[0], point[1]-1))
  if valid((point[0]-1, point[1]), data) and data[point[1]][point[0]] == data[point[1]][point[0]-1]:
    result.append((point[0]-1, point[1]))

  return result

def find_plot(point, data, plotset):

  if point in plotset:
    return plotset

  plotset.add(point)
  for n in neighbors(point, data):
    find_plot(n, data, plotset)
  data[point[1]][point[0]] = '.'

  return plotset
       

def part2(data):

  result = 0
  backup = copy.deepcopy(data)
  plots = defaultdict(set)
  plotnum = 0

  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if val != '.':
        plots[val + str(plotnum)] = find_plot((x,y), data, set())
        plotnum += 1

  for plotname,plotdata in plots.items():
    result += cost2(plotdata, backup)

  return(result)
  
def part1(data):

  result = 0
  backup = copy.deepcopy(data)
  plots = defaultdict(set)
  plotnum = 0

  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if val != '.':
        plots[val + str(plotnum)] = find_plot((x,y), data, set())
        plotnum += 1

  for plotname,plotdata in plots.items():
    result += cost1(plotdata, backup)

  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [list(line.strip()) for line in fileinput.input()]

    before = time.time()
    result = part1(copy.deepcopy(lines))
    after = time.time()
    print("part 1 results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))
