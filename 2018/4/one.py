#!/usr/bin/python3

import sys
import fileinput
import difflib
import re
from dateutil.parser import parse

gaurd = -1
count = dict()
total = dict()
ans2 = 0

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        date = parse(source.split(']')[0].strip('['))
        verb_r = source.split(']')[1:]
        verb = verb_r[0].strip()
        g = re.match( r"Guard #([0-9]+) begin", verb)
        if g:
            gaurd = g.group(1)
        elif (verb == 'falls asleep'):
            sleep = date
            print("gaurd: %s   sleep at minute: %d" % (gaurd, int(sleep.strftime("%M"))))
        elif (verb == 'wakes up'):
            for min in range(int(sleep.strftime('%M')), int(date.strftime('%M'))):
                count.setdefault(gaurd,{})[min] = count.setdefault(gaurd,{}).setdefault(min,0) + 1
                total[gaurd] = total.get(gaurd,0) + 1
                if (count[gaurd][min] >= ans2):
                    ans2 = count[gaurd][min]
                    print("Newer Answer 2: gaurd: %s  min: %d  count: %d  VALUE: %d" % (gaurd, min, count[gaurd][min], int(gaurd) * min))
        else:
            print("unkwon input: %s" % (source))

    largest=list(total.keys())[0]
    for each in total.keys():
#        print("gaurd: %s  %d min" % (each, total[each]))
        # Find the gaurd with the highest total
        if (total[each] > total[largest]):
            largest = each

    largemin=list(count[largest].keys())[0]
    for each in count[largest].keys():
#        print("gaurd: %s  min: %d  count: %d" % (largest, each, count[largest][each]))
        if (count[largest][each] > count[largest][largemin]):
            largemin = each

#    print("Largest is: gaurd: %s  sleep: %d min  most slept min: %d" % (largest, total[largest], largemin))
    print("Answer One: %d" % (int(largest) * largemin))
