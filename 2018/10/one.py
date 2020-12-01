#!/usr/bin/python

import sys
import re
import numpy as np
import Gnuplot


graph = dict()
x = []
y = []
vx = []
vy = []

g = Gnuplot.Gnuplot()
g.title("rainfall intensity")

g.xlabel("t (min)")
g.ylabel("i (mm/min)")

g("set grid")
g("set xtic 10")
g("set ytic 1")

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        g = re.match( r"position=<[ ]*(-?[0-9]+),[ ]*(-?[0-9]+)> velocity=<[ ]*(-?[0-9]+),[ ]*(-?[0-9]+)>", source)
        if g:
            x.append(int(g.group(1)))
            y.append(int(g.group(2)))
            vx.append(int(g.group(3)))
            vy.append(int(g.group(4)))
        else:
            print("unkwon input: %s" % (source))

d1 = Gnuplot.Data (x, y, title="step 1)", with_="lines")
#g("set terminal svg")
g.plot(d1) # write SVG data directly to stdout ...

