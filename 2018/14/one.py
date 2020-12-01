#!/usr/bin/python3

import sys
import re
import operator

data = [3, 7]
elfs = [0, 1]  # indexes into data

r=2

limit = int(sys.argv[1]);

while (r < limit+10):
#    print("#%d  len:%d  e0: %d e1: %d" % (r, len(data), elfs[0], elfs[1]))
    new = data[elfs[0]] + data[elfs[1]]
#    print("  new: %d + %d = %d" % (data[elfs[0]], data[elfs[1]], new))
    data += [int(x) for x in list(str(new))]
#    print("  data: %s" % (data))

#    print("  cur e0: %d  next e0: = (1 + %d) %% %d = %d" % (elfs[0], data[elfs[0]], len(data), elfs[0] + (1 + data[elfs[0]]) % len(data)))
#    print("  cur e1: %d  next e1: = (1 + %d) %% %d = %d" % (elfs[1], data[elfs[1]], len(data), elfs[1] + (1 + data[elfs[1]]) % len(data)))
    elfs[0] = (elfs[0] + 1 + data[elfs[0]]) % len(data)
    elfs[1] = (elfs[1] + 1 + data[elfs[1]]) % len(data)
#    print("#%d: %s  @%d  @%d" % (r, data, elfs[0], elfs[1]))

#    print("#%d: %s" % (r, data))
    if (r >= 10):
        score = ''
        i=r-9
        while i <= r:
            score += str(data[i])
            i += 1
        print("  score #%d: %s" % (r-9, score))

    r += 1

#print("")
#print("Anser #1 after %d recipes: %s\n" % (limit, score))

#tried 17415
