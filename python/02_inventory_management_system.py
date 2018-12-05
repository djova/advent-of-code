#!/usr/bin/env python

from collections import Counter
from itertools import chain, combinations
from os.path import join, realpath, dirname

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '02.txt')


def part_1():
    # 13m
    ids = [l.strip() for l in open(input_file)]
    docs_per_count = Counter(chain(*[set(Counter(s).values()) for s in ids]))
    print docs_per_count[2] * docs_per_count[3]


def diff_char_count(a, b):
    return sum([1 for x, y in zip(a, b) if x != y])


def part_2():
    # 12m
    ids = [l.strip() for l in open(input_file)]
    candidates = [(a, b) for a, b in combinations(ids, 2) if diff_char_count(a, b) == 1]

    if len(candidates) != 1:
        raise Exception("didn't find exactly one pair")

    print ''.join([x for x, y in zip(*candidates[0]) if x == y])


part_1()
part_2()
