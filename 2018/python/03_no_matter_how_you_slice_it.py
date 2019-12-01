#!/usr/bin/env python

import re
from collections import namedtuple
from os.path import join, realpath, dirname

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '03.txt')

Claim = namedtuple('Claim', ['id', 'x', 'y', 'w', 'h'])


def load_claims():
    def _parse(line):
        # #1 @ 808,550: 12x22
        ints = [int(i) for i in re.match("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line.strip()).groups()]
        return Claim(*ints)

    return [_parse(line) for line in open(input_file)]


def increment_claim(rect, c):
    for x in range(c.x, c.x + c.w):
        for y in range(c.y, c.y + c.h):
            rect[x][y] += 1


def no_overlap(rect, c):
    for x in range(c.x, c.x + c.w):
        for y in range(c.y, c.y + c.h):
            if rect[x][y] > 1:
                return False
    return True


def part_1():
    # 21m
    claims = load_claims()
    max_x = max([c.x + c.w for c in claims])
    max_y = max([c.y + c.h for c in claims])
    rect = [[0 for _ in range(max_y)] for _ in range(max_x)]

    for c in claims:
        increment_claim(rect, c)

    # count overlapping
    print sum(sum(1 if c > 1 else 0 for c in row) for row in rect)

    return rect, claims


def part_2():
    # 3m
    rect, claims = part_1()

    for c in claims:
        if no_overlap(rect, c):
            print c.id
            break
    else:
        raise Exception("failed to find non-overlapping claim")


part_2()
