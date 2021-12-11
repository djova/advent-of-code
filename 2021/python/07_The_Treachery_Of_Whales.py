#!/usr/bin/env python3
from collections import Counter, defaultdict
from os.path import join, dirname, realpath

import re

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '07.txt')
raw_input = open(input_file, 'r').read()

# reproduction rate: double every 7 days
# 2 days for 1st cycle of new fish

test_input1 = """\
16,1,2,0,4,2,7,1,2,14
"""


# 1: 1
# 2: 3
# 3: 6
# 4: 10
# 5: 15
# 6: 21

def parse(raw):
    return [int(x) for x in re.findall(r"\d+", raw)]


def move_cost(s, advanced=False):
    if advanced:
        return s * (1 + s) / 2
    else:
        return s


def align(crabs, advanced=False):
    # bruteforce
    mincost, minpos = None, None
    for i in range(max(crabs) + 1):
        cost = sum([move_cost(abs(c - i), advanced) for c in crabs])
        if not mincost or cost < mincost:
            mincost = cost
            minpos = i
    return f"aligned: {minpos}. fuel: {mincost}, advanced: {advanced}"


print("Part 1 (test): ", align(parse(test_input1), False))
print("Part 2 (test): ", align(parse(test_input1), True))
print("Part 1: ", align(parse(raw_input), False))
print("Part 2: ", align(parse(raw_input), True))
