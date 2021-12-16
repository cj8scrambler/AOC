#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import statistics
import copy
import math
import binascii
from collections import deque
from collections import Counter
from functools import reduce

# Packet Types
packetType = {
        '+': 0,
        '*': 1,
        'min': 2,
        'max': 3,
        'literal': 4,
        '>': 5,
        '<': 6,
        '==': 7 }

versum = 0

# returns (value, bits_consumed)
def handle_packet(data):
    global versum
    ver = int(data[0:3],2)
    versum += ver
    ptype = int(data[3:6],2)
    logging.debug("  packet ver={}  type={}".format(ver,ptype))
    offset = 6
    if ptype == packetType['literal']:
        val = ''
        ntype = '1'
        # Keep reading nibbles til one begins with a 0, that's the last noe
        while ntype == '1':
            ntype = data[offset]
            val += data[offset+1:offset+5]
            offset += 5
        logging.debug("    read literal: {} from ({})".format(int(val,2), val))
        return(int(val,2), offset)

    # All other packet types are operaters which have
    # multiple arguments packed as literal sub-packets
    else:
        args=[]
        lentype = data[offset]
        offset += 1
        if lentype == '0':
            subpacketsize = int(data[offset:offset+15], 2)
            offset += 15 
            logging.debug("    operator lengtype-0 subpackets: {} bytes".format(subpacketsize))
            while subpacketsize > 0:
                (val, length) = handle_packet(data[offset:])
                args.append(val)
                subpacketsize -= length
                offset += length
        else:
            numsubpackets = int(data[offset:offset+11], 2)
            offset += 11
            logging.debug("    operator lengtype-1 {} subpackets".format(numsubpackets))
            for sp in range(numsubpackets):
                (val, length) = handle_packet(data[offset:])
                args.append(val)
                offset += length
        logging.debug("  Got arguments {}".format(args))

        if ptype == packetType['+']:
            result = 0
            for a in args:
                result += a
            logging.info("  SUM ({}) = {}".format(args, result))
            return (result, offset)
        if ptype == packetType['*']:
            result = 1
            for a in args:
                result *= a
            logging.info("  PRODUCT({}) = {}".format(args, result))
            return (result, offset)
        if ptype == packetType['min']:
            result = math.inf
            for a in args:
                if a < result:
                    result = a
            logging.info("  MIN({}) -> {}".format(args, result))
            return (result, offset)
        if ptype == packetType['max']:
            result = -math.inf
            for a in args:
                if a > result:
                    result = a
            logging.info("  MAX({}) -> {}".format(args, result))
            return (result, offset)
        if ptype == packetType['<']:
            logging.info("  {} < {} -> {}".format(args[0], args[1], int(args[0] < args[1])))
            return (int(args[0] < args[1]), offset)
        if ptype == packetType['>']:
            logging.info("  {} > {} -> {}".format(args[0], args[1], int(args[0] > args[1])))
            return (int(args[0] > args[1]), offset)
        if ptype == packetType['==']:
            logging.info("  {} == {} -> {}".format(args[0], args[1], int(args[0] == args[1])))
            return (int(args[0] == args[1]), offset)

    raise("Unhandled packet type: {}".format(ptype))


def hextobin(h):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    data = ''
    for line in fileinput.input():
        logging.debug("convert {} to {}".format(line.rstrip(), hextobin(line.rstrip())))
        data += hextobin(line.rstrip())

    logging.debug('data: {}'.format(data))

    before = time.time()
    (result,length) = handle_packet(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(versum, (after - before)))

    before = time.time()
    (result,length) = handle_packet(data)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))
