#!/usr/bin/env python3
import re
from collections import defaultdict, Counter
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '14.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


def parse(raw):
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    template = lines[0]
    mapping = {k: v for k, v in [l.split(' -> ') for l in lines[1:]]}
    return template, mapping


def polymerize(polymer, mapping):
    last = None
    for c in polymer:
        if not last:
            last = c
            continue
        yield last
        if insertion := mapping.get(last + c):
            yield insertion
        last = c
    yield last


def go(polymer, mapping, iterations):
    for _ in range(iterations):
        polymer = polymerize(polymer, mapping)

    counts = defaultdict(int)
    for p in polymer:
        counts[p] += 1
    most_common = max([v for k, v in counts.items()])
    least_common = min([v for k, v in counts.items()])
    length = sum(counts.values())
    return f"completed {iterations} iterations. length={length} max-min={most_common - least_common} "


print("test", go(*parse(test_input1), iterations=10))

print("part 1", go(*parse(raw_input), iterations=10))
# print("part 2", go(*parse(raw_input), iterations=40))
