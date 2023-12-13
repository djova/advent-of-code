#!/usr/bin/env python3
import functools
import itertools
import math
import re
from collections import Counter
from enum import Enum
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '08.txt')
input_text = open(input_file, 'r').read()


def parse_raw_input(raw_input):
    lines = [l.strip() for l in raw_input.split('\n') if l.strip()]
    steps = lines[0]
    tuples = [re.findall(r'[0-9A-Z]+', l) for l in lines[1:]]
    graph = {s: (l, r) for s, l, r in tuples}
    return steps, graph


test_input_1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

test_input_2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

test_input_3 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def steps_to_end(raw_input):
    steps, graph = parse_raw_input(raw_input)
    p = "AAA"
    steps_taken = 0
    for s in itertools.cycle(steps):
        if p == "ZZZ":
            return steps_taken
        p = graph[p][0] if s == 'L' else graph[p][1]
        steps_taken += 1


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def steps_to_end_parallel(raw_input):
    steps, graph = parse_raw_input(raw_input)
    positions = [k for k in graph.keys() if k.endswith('A')]
    lengths = []
    for p in positions:
        steps_taken = 0
        for s in itertools.cycle(steps):
            if p.endswith('Z'):
                lengths.append(steps_taken)
                break
            p = graph[p][0] if s == 'L' else graph[p][1]
            steps_taken += 1
    return functools.reduce(lcm, lengths)


def test_steps_to_end():
    assert steps_to_end(test_input_1) == 2
    assert steps_to_end(test_input_2) == 6


def test_steps_to_end_parallel():
    assert steps_to_end_parallel(test_input_3) == 6


def run_main():
    print("part 1:", steps_to_end(input_text))
    print("part 2:", steps_to_end_parallel(input_text))


if __name__ == '__main__':
    run_main()
