#!/usr/bin/python3

def increases(val):
    num = str(val);
    if ((num[0] <= num[1]) and (num[1] <= num[2]) and (num[2] <= num[3]) and (num[3] <= num[4]) and (num[4] <= num[5])):
        print("  increases: %d  true" % (val))
        return True
    return False

def hasdouble(val):
    num = str(val);
    if ((num[0] == num[1]) or (num[1] == num[2]) or (num[2] == num[3]) or (num[3] == num[4]) or (num[4] == num[5])):
        print("  has double: %d  true" % (val))
        return True
    return False

matches=0
for att in range(145852, 616942):
    if (increases(att) and hasdouble(att)):
        matches += 1
        print("valid: %d  sum: %d" % (att, matches))
