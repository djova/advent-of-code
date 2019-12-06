#!/usr/bin/env python3
import math
from os.path import join, dirname, realpath

from lib.intcode import runcode


def meets(x):
    has_double = False
    last = None
    matching = 0
    for c in str(x):
        if last is None:
            last = c
            matching = 1
        elif int(c) < int(last):
            # decreased
            return False
        elif c == last:
            matching += 1
        else:
            # changed
            if matching > 1:
                if matching == 2:
                    has_double = True
            last = c
            matching = 1
    if matching > 1:
        if matching == 2:
            has_double = True
    return has_double


def run_tests():
    if meets(111111):
        print("fail")
    elif meets(223450):
        print("fail")
    elif meets(123789):
        print("fail")
    elif not meets(112233):
        print("fail")
    elif meets(123444):
        print("fail")
    elif not meets(111122):
        print("fail")
    else:
        print("tests passed")


run_tests()


def count_passwords():
    meet_count = 0
    for x in range(347312, 805915 + 1):
        if meets(x):
            meet_count += 1
    return meet_count


print(count_passwords())
