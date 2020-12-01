#!/usr/bin/python3

import sys
import re
import operator

track = []
trains = []

def print_map():
    y = 0
    train = 0
    while y < len(track):
        x = 0
        while x < len(track[y]):
            if ((train < len(trains)) and
                (trains[train]['loc_x'] == x) and
                (trains[train]['loc_y'] == y)):
                print("%c" % (trains[train]['name']), end="")
#                print("[%d,%d] : train-%c" % (y, x, trains[train]['name']))
                train += 1
            else:
                print("%c" % (track[y][x]), end="")
#                print("[%d,%d] : track: %c" % (y, x, track[y][x]))
#            if (train < len(trains)):
#                if (y is 1) and (x is 12):
#                    print("Special case: [1,12]  train=%d :" % (train))
#                    print(trains[train])

            x +=1
        print("");
        y +=1

def crash_detect():
    global trains
    global track

    dups = [] #map of dups
    crashes = [] #list of crash coordinates

    #make an empty map
    for y in track:
        dups.append([''] * len(y))

    #map the trains looking for a dup
    for train in trains:
        if (dups[train['loc_y']][train['loc_x']] is 'x'):
            print("\nCrash detected at: [%d,%d]" % (train['loc_x'], train['loc_y']));
            crashes.append( (train['loc_y'], train['loc_x']) )
        else:
            dups[train['loc_y']][train['loc_x']] = 'x'

    # remove all the crashes
    for coord in crashes:
        # itterate on a copy of trains since we're removing entries
        for train in trains[:]:
            if ((train['loc_y'] is coord[0]) and
                (train['loc_x'] is coord[1])):
                print("Removing train-%c at [%d,%d]" % (train['name'], train['loc_y'], train['loc_x']))
                trains.remove(train)

    return 0

def tick():
    global trains
    global track

    trains = sorted(trains, key=lambda k: k['loc_y'])
    #print ("Sorted list of trains:\n%s" % (trains))

    for train in trains[:]:
        #print("Moving train-%c" % (train['name']))
        if (track[train['loc_y']][train['loc_x']] is '|'):
            if (train['dir'] is 0):     # going north
                train['loc_y']  -= 1
                #print("moved train %c north" % (train['name']))
            elif (train['dir'] is 1):   # going east
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))
            elif (train['dir'] is 2):   # going south
                train['loc_y']  += 1
                #print("moved train %c south" % (train['name']))
            elif (train['dir'] is 3):   # going west
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))
            else:
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))

        elif (track[train['loc_y']][train['loc_x']] is '-'):
            if (train['dir'] is 0):     # going north
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))
            elif (train['dir'] is 1):   # going east
                train['loc_x']  += 1
                #print("moved train %c east" % (train['name']))
            elif (train['dir'] is 2):   # going south
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))
            elif (train['dir'] is 3):   # going west
                train['loc_x']  -= 1
                #print("moved train %c west" % (train['name']))
            else:
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))

        elif (track[train['loc_y']][train['loc_x']] is '/'):
            if (train['dir'] is 0):     # going north
                train['dir'] = 1        # change to east
                train['loc_x']  += 1
                #print("changed train %c dir to east and moved east" % (train['name']))
            elif (train['dir'] is 1):   # going east
                train['dir'] = 0        # change to north
                train['loc_y']  -= 1
                #print("changed train %c dir to north and moved north" % (train['name']))
            elif (train['dir'] is 2):   # going south
                train['dir'] = 3        # change to west
                train['loc_x']  -= 1
                #print("changed train %c dir to west and moved west" % (train['name']))
            elif (train['dir'] is 3):   # go west
                train['dir'] = 2        # change to south
                train['loc_y']  += 1
                #print("changed train %c dir to south and moved south" % (train['name']))
            else:
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))

        elif (track[train['loc_y']][train['loc_x']] is '\\'):
            if (train['dir'] is 0):     # going north
                train['dir'] = 3        # change to west
                train['loc_x']  -= 1
                #print("changed train %c dir to west and moved west" % (train['name']))
            elif (train['dir'] is 1):   # going east
                train['dir'] = 2        # change to south
                train['loc_y']  += 1
                #print("changed train %c dir to south and moved south" % (train['name']))
            elif (train['dir'] is 2):   # going south
                train['dir'] = 1        # change to east
                train['loc_x']  += 1
                #print("changed train %c dir to east and moved east" % (train['name']))
            elif (train['dir'] is 3):   # go west
                train['dir'] = 0        # change to north
                train['loc_y']  -= 1
                #print("changed train %c dir to north and moved north" % (train['name']))
            else:
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))

        elif (track[train['loc_y']][train['loc_x']] is '+'):
            if (train['next'] is 'L'):
                train['dir']  = (train['dir'] - 1) % 4
                train['next']  = 'C'
                #print("changed train %c dir to %d " % (train['name'], train['dir']), end="")
            elif (train['next'] is 'C'):
                train['next']  = 'R'
                #print("kept train %c dir as %d " % (train['name'], train['dir']), end="")
            elif (train['next'] is 'R'):
                train['dir']  = (train['dir'] + 1) % 4
                train['next']  = 'L'
                #print("changed train %c dir to %d " % (train['name'], train['dir']), end="")
            else:
                raise Exception("Invalid: train(%d,%d) heading %d on track '%c'" % (train['loc_x'], train['loc_y'], train['dir'], track[train['loc_y']][train['loc_x']]))

            if (train['dir'] is 0):     # going north
                train['loc_y']  -= 1
                #print("and moved north");
            elif (train['dir'] is 1):   # going east
                train['loc_x']  += 1
                #print("and moved east");
            if (train['dir'] is 2):     # going south
                train['loc_y']  += 1
                #print("and moved south");
            elif (train['dir'] is 3):   # going west
                train['loc_x']  -= 1
                #print("and moved west");

        crash_detect()

    trains = sorted(trains, key=lambda k: (k['loc_y'], k['loc_x']))

    return 0

with open(sys.argv[1], 'r') as source_f:
    y=0
    name=ord('A')
    for source in source_f:
        track.append(list(source.rstrip()))
        x = 0
        while (x < len(track[y])):
            if (track[y][x] is '<'):
                track[y][x] = '-'
                trains.append({'loc_x': x, 'loc_y': y, 'next': 'L', 'dir': 3, 'name': chr(name)})
                name += 1
            if (track[y][x] is '>'):
                track[y][x] = '-'
                trains.append({'loc_x': x, 'loc_y': y, 'next': 'L', 'dir': 1, 'name': chr(name)})
                name += 1
            if (track[y][x] is 'v'):
                track[y][x] = '|'
                trains.append({'loc_x': x, 'loc_y': y, 'next': 'L', 'dir': 2, 'name': chr(name)})
                name += 1
            if (track[y][x] is '^'):
                track[y][x] = '|'
                trains.append({'loc_x': x, 'loc_y': y, 'next': 'L', 'dir': 0, 'name': chr(name)})
                name += 1
            x += 1
        y += 1
                
    print_map()

    i = 0
    run = 1
    print("Running", end="")
    while (run):
#        print("")
#        print_map()
        tick()
        i += 1
        if (len(trains) <= 1):
            print("\nOnly %d trains left" % (len(trains)))
            for train in trains:
                print("  train-%c: [%d,%d]" % (train['name'], train['loc_x'], train['loc_y']))
            run = 0

print("Took %d ticks" % (i-1))
