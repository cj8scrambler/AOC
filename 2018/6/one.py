#!/usr/bin/python3

import sys
import re

map = {}
i = 0
ids = []
xrange = 0
yrange = 0
largest = {}

def distance(x1, y1, x2, y2):
    return (abs(x1 - x2) + abs(y1 - y2))

with open(sys.argv[1], 'r') as source_f:
    # Create a sparse map of original data points
    for source in source_f:
        x = int(source.split(',')[0].strip())
        y = int(source.split(',')[1].strip())
#        print ("%d,%d" % (x,y))
        map.setdefault(x,{})[y] = {'id': chr(ord('A') + i), 'distance': 0, 'count': 0}
        ids.append({'id': chr(ord('A') + i), 'x': x, 'y': y})
        if (x > xrange):
            xrange = x
        if (y > yrange):
            yrange = y
        i += 1

    #input data is 0 based; so increment ranges
    xrange += 1
    yrange += 1
#    print ("xrange: %d  yrange: %d" % (xrange, yrange))
    # print the map
    for y in range(yrange):
        for x in range(xrange):
            if (x in map) and (y in map[x]):
                print ("%s " % (map[x][y]['id']), end="")
            else:
                print ("%s " % ('.'), end="")
        print("")
           
    # map nearest points
    for y in range(yrange):
        for x in range(xrange):
            for node in ids:
                d = distance(x, y, node['x'], node['y'])
                if (x not in map) or (y not in map[x]) or (d < map[x][y]['distance']):
#                    print("Update %d,%d to %s-%d" % (x,y,node['id'],d))
#                    print("Currently: %s" % (map.setdefault(x,{}).setdefault(y,{}).get('distance',"unset")))
                    map.setdefault(x,{}).setdefault(y,{})['id'] = node['id']
                    map.setdefault(x,{}).setdefault(y,{})['distance'] = d
                    map.setdefault(x,{}).setdefault(y,{})['count'] = 1
                elif d == map[x][y]['distance']:
                    map.setdefault(x,{}).setdefault(y,{})['count'] += 1

    # print the map
    print("")
    print("")
    for y in range(yrange):
        for x in range(xrange):
            if (map[x][y]['count'] == 1):
                if (map[x][y]['distance'] == 0):
                    print ("%s " % (map[x][y]['id']), end="")
                else:
                    print ("%s " % (map[x][y]['id'].lower()), end="")
#                print ("%s-%02d  " % (map[x][y]['id'], map[x][y]['distance']), end="")
            else:
                print ("%s " % ('.'), end="")
#                print ("%s-%02d  " % ('.', map[x][y]['distance']), end="")
        print("")
           
    print("")
    print("")
    # find the largest non-edge area
    for each in ids:
        largest[each['id']] = 0;
    for y in range(yrange):
        for x in range(xrange):
#            print ("%d,%d" % (x, y))
            if (x == 0) or (x == (xrange - 1)) or (y == 0) or (y == (yrange - 1)):
                if map[x][y]['id'] in largest:
                    print ("Removing '%s' because it's on an edge at %d,%d" % (map[x][y]['id'], x, y))
#                    largest[map[x][y]['id']]  -= 100000
                    del largest[map[x][y]['id']]
            else:
                if map[x][y]['id'] in largest:
                    largest[map[x][y]['id']] += 1

    maxarea = 0
    for each in largest.keys():
        if largest[each] > maxarea:
            maxarea = largest[each]

    print (largest)

    print("")
    print ("Largest area: %d" % (maxarea))
