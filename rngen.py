import string 
import random

# Victor Kuciel 
# CPEG 472: Applied Cryptography
# Project 2 - Break C's random number generator


########################################################
# Python's implementation of the random number generator
# https://gist.github.com/AndyNovo/94b9974a4945392bc8f4414b6509ca65

def crand(seed):
    r=[]
    r.append(seed)
    for i in range(30):
        r.append((16807*r[-1]) % 2147483647)
        if r[-1] < 0:
            r[-1] += 2147483647
    for i in range(31, 34):
        r.append(r[len(r)-31])
    for i in range(34, 344):
        r.append((r[len(r)-31] + r[len(r)-3]) % 2**32)
    while True:
        next = r[len(r)-31]+r[len(r)-3] % 2**32
        r.append(next)
        yield (next >> 1 if next < 2**32 else (next % 2**32) >> 1)

######################################################

def initialVal(numb):
    changed = True
    unknown = [-1] * 93

    while changed:
        changed = False

        for integer in range(31, 93):
            changed = valInspect(numb, unknown, integer, changed)
    return unknown

def valInspect(numb, unknown, integer, changed):
    end1 = (2*(numb[integer] - numb[integer-3] - numb[integer-31])) % 2**32

    if end1 == 2:
        n1 = complete(unknown, integer, 0)
        n2 = complete(unknown, integer-3, 1)
        n3 = complete(unknown, integer-31, 1)
        changed = changed or n1 or n2 or n3

    else:
        if unknown[integer] == 0:
            n1 = complete(unknown, integer-3, 0)
            n2 = complete(unknown, integer-31, 0)
            changed = changed or n1 or n2
        if integer - 3 >= 0 and unknown[integer-3] == 1:
            n1 = complete(unknown, integer-31, 0)
            n2 = complete(unknown, integer, 1)
            changed = changed or n1 or n2
        if integer - 31 >= 0 and unknown[integer-31] == 1:
            n1 = complete(unknown, integer-3, 0)
            n2 = complete(unknown, integer, 1)
            changed = changed or n1 or n2

    return changed

def complete(numb, link, value):

    if numb[link] == -1:
        numb[link] = value
        return True

    else:
        return False

def valR(numb, u1):
    iVAL = [-1]*93

    for integer in range(93):
        if not (u1[integer] == -1):
            calc(numb, u1, iVAL, integer)

    return iVAL

def calc(obs, mys, r, integer):
    r[integer] = (obs[integer] * 2 + mys[integer]) % 2**32

def precedingCal(r, integer):
    valsOfPre = (r[integer-3] == -1 or r[integer-31] == -1)

    if not valsOfPre:
        calc = (r[integer-3] + r[integer-31]) % 2**32
        r[integer] = calc
    if integer + 3 < len(r) and not(r[integer+3] == -1 or r[integer-28] == -1):
        calc = (r[integer+3] - r[integer-28]) % 2**32
        r[integer] = calc
    if integer + 31 < len(r) and not(r[integer+31] == -1 or r[integer+28] == -1):
        calc = (r[integer+31] - r[integer+28]) % 2**32
        r[integer] = calc

def bruteForce(r, u1, val1):   # Make nested loop

    for integer in range(31, 93): 
        if r[integer] == -1:
            for n1 in range(2):
                u1[integer] = n1
                if proveNum(r, u1, val1, integer):
                    break
                else:
                    u1[n1] = -1

def proveNum(r, mys, obs, n1):
    if n1 < 0 or n1+28 > 93:
        return True

    if (r[n1] == (r[n1-3] + r[n1-31]) % 2**32):
        if (not(mys[n1] == -1) and (2 * obs[n1] + mys[n1]) % 2** 32 == r[n1]):
            return True
        else:
            return False

    return proveNum(r,mys,obs, n1+3) and proveNum(r,mys,obs, n1+28)

def conclusion(r, u1, val1):
    for integer in range(62, 93):
        if r[integer] == -1:
            if not(u1[integer] == -1):
                calc(val1,u1,r,integer)

def calcFollowingN(r, iOfN):
    iOfN += 93
    calc =(r[iOfN-3] + r[iOfN-31]) % 2**32
    r.append(calc)

    return calc >> 1

def calcFollowing93(r):
    output = []
    for integer in range(93):
        output.append(calcFollowingN(r,integer))

    return output

def verifyAll(alist):
    rgen = 0

    for integer in range(alist):                 # module2
        theseed = random.randint(1, 2**30)
        skip = random.randint(10000, 200000)

        my_generator = crand(theseed)
        for i in range(skip):
            temp = my_generator.next()

        the_input = [my_generator.next() for i in range(93)]
        the_output = [my_generator.next() for i in range(93)]

        test = your_code(the_input)
        if test == the_output:
            rgen += 1
    return rgen, alist

def your_code(theinput):
    unknownValue = initialVal(theinput)
    r = valR(theinput, unknownValue)
    for integer in range(31,93):
        precedingCal(r, integer)
    bruteForce(r, unknownValue, theinput)
    conclusion(r, unknownValue, theinput)
    output = calcFollowing93(r)

    return output

outcome = verifyAll(200) # 200 to verify
print str(outcome[0]) + " / " + str(outcome[1]) + " passed, You Win!"   # This may take about 20 seconds to verify all
