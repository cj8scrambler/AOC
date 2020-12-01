#!/usr/bin/python3

import sys
import re

# Base time it takes to complete a task
BASE_TIME = 60

graph = dict()

def find_last(thegraph):
    ''' Find a target that doesn't have a source (the last step)'''''
    targets = dict()
    for source in thegraph.keys():
        for target in thegraph[source]:
            targets[target] = 1
#    print("all possible targets: %s" % (targets))
    for each in thegraph.keys():
        if each in targets:
#            print("it's not '%s'" % (each))
            del targets[each]
    
#    print("That leaves: %s" % (targets))
    if (len(targets) == 0):
        raise ValueError('Circular graph')

    return list(targets.keys())[0]

def next_worker(thelist):
    ''' Find an avaialble worker; if no workers, return -1 '''

    for i,task in enumerate(d['task'] for d in thelist):
        if (task == ''):
            return i
    return -1

def find_available(thegraph):
    ''' Return an alphabeticly sorted list of available tasks (no depednecies) in the graph '''
    possible = list(thegraph.keys())
    for source in thegraph.keys():
        for target in thegraph[source]:
            if target in possible:
                possible.remove(target);
    if (len(possible) == 0):
        raise ValueError('Circular graph')

    return sorted(possible)
    
with open(sys.argv[1], 'r') as source_f:
    # Create a directed graph of the tasks (dictionary of lists)
    for source in source_f:
        before = ''
        after = ''
        g = re.match( r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.", source)
        if g:
            before = g.group(1)
            after = g.group(2)
        else:
            print("unkwon input: %s" % (source))

#        print ("%s -> %s" % (before, after))
        graph.setdefault(before,[]).append(after)

    # Make a special entry for the last element (has no 'after' step)
    last = find_last(graph)
    graph[last] = []

    # Make a backup copy so we can re-use this for problem #2
    graph2 = dict(graph)

    print("Answer one:")
    while(graph):
        next = find_available(graph)[0]
        print("%s" % (next), end="")
        del graph[next]
    print("")

    # Restore the original directed graph
    graph = graph2
    inprogress = []
    workers = [ {'task': '', 'time': 0}, {'task': '', 'time': 0}, {'task': '', 'time': 0}, {'task': '', 'time': 0}, {'task': '', 'time': 0} ]
    time = 0

    print("Answer two:")
    while(graph):
        # get available tasks and remove those already in progress
        available = find_available(graph)
        for each in available[:]:
            if each in inprogress:
                available.remove(each)

        # for each available task assign any available workers
        for next in sorted(available):
            worker = next_worker(workers)
            if (worker >= 0):
                workers[worker]['task'] = next
                workers[worker]['time'] = ord(next) - 64 + BASE_TIME
                inprogress.append(next)
                print("%d: assign worker %d task %s (takes %d secs)" % (time, worker, workers[worker]['task'], workers[worker]['time']))

        # decrement time for each workers task; check if they've finsished
        # if finished:
        #     remove from inprgrogess list (could have checked done this without a seperate list)
        #     remove from the original directed graph
        #     mark the worker as free (no task)
        for each in workers:
            each['time'] -= 1
            if each['time'] == 0:
                print("%d: worker finished task %s" % (time, each['task']))
                inprogress.remove(each['task'])
                del graph[each['task']]
                each['task'] = ''

#        print("%d: working...." % (time))
        # time moves on
        time += 1
    print("Total time: %d" % (time))
