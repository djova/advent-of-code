#!/usr/bin/env python3
from builtins import int

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


def insertion_locs(loc):
    if loc == 'left':
        return 'left', 'middle'
    elif loc == 'right':
        return 'middle', 'right'
    else:
        return 'middle', 'middle'


class Polymer:
    def __init__(self, raw, mapping):
        self.pmap = {}
        self.mapping = mapping
        for i in range(len(raw) - 1):
            p = raw[i:i + 2]
            if i == 0:
                self.add('left', p)
            elif i == len(raw) - 2:
                self.add('right', p)
            else:
                self.add('middle', p)

    def add(self, loc, p, v=1):
        key = (loc, p)
        if key not in self.pmap:
            self.pmap[key] = 0
        self.pmap[key] += v

    def polymerize(self):
        result = Polymer("", self.mapping)
        for (loc, p), v in self.pmap.items():
            if insertion := self.mapping.get(p):
                left, right = insertion_locs(loc)
                result.add(left, p[0] + insertion, v)
                result.add(right, insertion + p[1], v)
            else:
                result.add(loc, p, v)
        return result

    def polymer_counts(self):
        counts = defaultdict(int)
        middle_counts = defaultdict(int)
        for (loc, p), v in self.pmap.items():
            if loc == 'left':
                counts[p[0]] += v
                middle_counts[p[1]] += v
            elif loc == 'right':
                middle_counts[p[0]] += v
                counts[p[1]] += v
            else:
                for c in p:
                    middle_counts[c] += v

        for c, v in middle_counts.items():
            if v % 2 != 0:
                raise Exception("must be even")
            counts[c] += v // 2

        return counts


def go(polymer, mapping, iterations):
    poly = Polymer(polymer, mapping)
    for _ in range(iterations):
        poly = poly.polymerize()

    counts = poly.polymer_counts()
    most_common = max([v for k, v in counts.items()])
    least_common = min([v for k, v in counts.items()])
    length = sum(counts.values())
    return f"completed {iterations} iterations. length={length} max-min={most_common - least_common} "


print("test", go(*parse(test_input1), iterations=1))
print("test", go(*parse(test_input1), iterations=10))

print("part 1", go(*parse(raw_input), iterations=10))
print("part 2", go(*parse(raw_input), iterations=40))
