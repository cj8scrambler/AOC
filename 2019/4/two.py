#!/usr/bin/python3

def increases(val):
    num = str(val);
    if ((num[0] <= num[1]) and (num[1] <= num[2]) and (num[2] <= num[3]) and (num[3] <= num[4]) and (num[4] <= num[5])):
#        print("  increases: %d  true" % (val))
        return True
    return False

def hasdouble(val):
    pair = 0
    num = str(val);

    if (num[0] == num[1]):
        pair += 1
    if (num[1] == num[2]):
        pair += 1
    if (num[2] == num[3]):
        pair += 1
    if (num[3] == num[4]):
        pair += 1
    if (num[4] == num[5]):
        pair += 1

    if pair == 1:
        print("  has 1 double: %d  true" % (val))
        return True
    return False

def hasadouble(val):
    pairlen = 1
    num = str(val);
    lastdigit = ' '
    #print(val)
    for digit in num:
        if lastdigit == digit:
            pairlen += 1
            #print(" %s: pairlen=%d" % (digit, pairlen))
        else:
            if (pairlen == 2):
                #print(" %s: pairlen=%d TRUE" % (digit, pairlen))
                return True
            pairlen = 1
            #print(" %s: pairlen=%d" % (digit, pairlen))
        lastdigit = digit

    if (pairlen == 2):
        #print(" %s: pairlen=%d last digit TRUE" % (digit, pairlen))
        return True
    return False

matches=0
for att in range(145852, 616943):
    if (increases(att) and hasadouble(att)):
        matches += 1
        print("  valid: %d  sum: %d" % (att, matches))
