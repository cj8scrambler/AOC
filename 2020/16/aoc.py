#!/usr/bin/python

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
  
def part1(rules, tickets):

    good = {}
    sumbad = 0
    retlist = []
    for rule in rules:
        for goodval in range(int(rule['r1b']), int(rule['r1e'])+1):
            good[goodval] = 1
        for goodval in range(int(rule['r2b']), int(rule['r2e'])+1):
            good[goodval] = 1

    logging.debug("Good values: {}".format(good))
    for ticket in tickets:
        logging.debug("on ticket: {}".format(ticket))
        bad = 0
        for num in ticket:
            if num not in good:
                logging.debug("  {} is bad".format(num))
                sumbad += num
                bad = 1
                break
        if not bad:
            logging.debug("  ticket is good".format(num))
            retlist.append(ticket)

    print("Part 1: {}".format(sumbad))
    return retlist

def part2(rules, tickets):

    logging.debug("Got tickets: {}".format(tickets))
    good = {}
    for rule in rules:
        good[rule['field']] = []
        for goodval in range(int(rule['r1b']), int(rule['r1e'])+1):
            good[rule['field']].append(goodval)
        for goodval in range(int(rule['r2b']), int(rule['r2e'])+1):
            good[rule['field']].append(goodval)

    logging.debug("Good values: {}".format(good))

    impossible = {}
    for ticket in tickets[1:]:
        for i in range(len(ticket)):
            for field in good:
                if ticket[i] not in good[field]:
                    logging.debug("column {} can't be {} because of ticket: {}".format(i, field, ticket))
                    if field in impossible:
                        impossible[field].append(i)
                    else:
                        impossible[field] = [i]
    logging.debug("Impossible fields: {}".format(impossible))

    possible = {}
    for field in good:
        possible[field] = range(len(tickets[0]))
        if field in impossible:
            for val in impossible[field]:
                possible[field].remove(val)

    logging.debug("Possible fields: {}".format(possible))
    # N^2 - Not good
    solution = {}
    while len(solution) < len(tickets[0]):
        logging.debug("Look for a field with 1 solution".format(field, val))
        for field in possible:
            logging.debug("  Length of {}: {} ({})".format(field, len(possible[field]), possible[field]))
            if (len(possible[field]) == 1):
                val = possible[field][0]
                logging.debug("  Found mandatory solution: {} = {}".format(field, val))
                solution[field] = val
                for cleanup in possible:
                    if val in possible[cleanup]:
                        logging.debug("  remove {} from possible[{}]".format(val, cleanup))
                        possible[cleanup].remove(val)
                break;

    logging.debug("Solution: {}".format(solution))

    product = 1
    logging.debug("find 'departure' fields in: {}".format(tickets[0]))
    for field in solution:
        if 'departure' in field:
            logging.debug("field col %d ('%s') on my ticket is: %d" % (solution[field], field, tickets[0][solution[field]]))
            product *= tickets[0][solution[field]]
            logging.debug("Adding field {} value: {} makes product: {}".format(field, tickets[0][solution[field]], product))

    return product


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    rules = []
    tickets = []   # my ticket is first

    on_rules = True

    # class: 1-3 or 5-7
    fieldpattern = re.compile(r"(?P<field>[\w ]+): (?P<r1b>\d+)-(?P<r1e>\d+) or (?P<r2b>\d+)-(?P<r2e>\d+)")

    for line in fileinput.input():
        if on_rules:
            match = fieldpattern.match(line)
            if match:
                logging.debug("line: {} rules match: {}".format(line, match.groupdict()))
                rules.append(match.groupdict())
            else:
                logging.debug("line: {} no rules match".format(line))
                on_rules = False
        else:
            data = []
            for num in line.rstrip().split(','):
                try:
                    data.append(int(num))
                except ValueError:
                    logging.debug("line: {} ignore match failure".format(line))

            if len(data):
                tickets.append(data)

    logging.debug("Rule Data: {}".format(rules))
    logging.debug("Ticket Data: {}".format(tickets))

    goodlist = part1(rules, tickets[1:])
    print("good list is {}".format(goodlist))

    result = part2(rules, [tickets[0]] + goodlist)
    print("Part 2: {}".format(result))
