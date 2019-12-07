#!/usr/bin/env python3
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '06.txt')
input_string = open(input_file, 'r').read()

test_input = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

test_input2 = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""


def parse_input(s):
    pairs = [l.split(')') for l in s.split('\n') if l]
    return {v: k for k, v in pairs}


def count_orbits_for_node(orbits, start):
    stack = [start]
    total = 0
    while stack:
        x = stack.pop()
        if x in orbits:
            total += 1
            stack.append(orbits[x])
    return total


def count_total_orbits(orbits):
    total = 0
    for x in orbits.keys():
        total += count_orbits_for_node(orbits, x)
    return total


def expand_path(orbits, start):
    current = start
    while current in orbits:
        current = orbits[current]
        yield current


# a -> b
def min_transfers(orbits, a, b):
    a_path = list(reversed(list(expand_path(orbits, a))))
    b_path = list(reversed(list(expand_path(orbits, b))))
    last_common_i = -1
    for i, (ai, bi) in enumerate(zip(a_path, b_path)):
        if ai == bi:
            last_common_i = i
        else:
            break
    if last_common_i < 0:
        raise Exception("nothing common")
    return len(a_path) + len(b_path) - 2 * (last_common_i + 1)


def run_test():
    total = count_total_orbits(parse_input(test_input))
    if total != 42:
        print("failed test")
    else:
        print("passed")

    result2 = min_transfers(parse_input(test_input2), "YOU", "SAN")
    if result2 != 4:
        print("failed transfers", result2)
    else:
        print("passed transfers")


run_test()

# part 1
orbits = parse_input(input_string)
print(count_total_orbits(orbits))

# part 2
print(min_transfers(orbits, "YOU", "SAN"))
