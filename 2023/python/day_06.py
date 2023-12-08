#!/usr/bin/env python3
import functools
import math
import re
from collections import defaultdict
from os.path import join, dirname, realpath

import pytest

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '06.txt')
input_text = open(input_file, 'r').read()


def parse_raw_input(raw_input):
    lines = [l.strip() for l in raw_input.split('\n') if l.strip()]
    return [[int(d) for d in re.findall('\d+', l)] for l in lines]


test_input = """\
Time:      7  15   30
Distance:  9  40  200
"""


def get_num_ways_to_win(raw_input, part2=False):
    times, records = parse_raw_input(raw_input)
    if part2:
        times = [int("".join([str(t) for t in times]))]
        records = [int("".join([str(t) for t in records]))]
    for t, r in zip(times, records):
        ways = 0
        for h in range(0, t):
            
            d = (t - h) * h
            if d > r:
                ways += 1
        yield ways


def get_win_product(raw_input, part2=False):
    return functools.reduce(lambda x, y: x * y, get_num_ways_to_win(raw_input, part2=part2))


def test_num_ways_to_win():
    assert list(get_num_ways_to_win(test_input)) == [4, 8, 9]
    assert get_win_product(test_input) == 288
    assert get_win_product(test_input, part2=True) == 71503


def run_main():
    print("part 1:", get_win_product(input_text))
    print("part 2:", get_win_product(input_text, part2=True))


if __name__ == '__main__':
    run_main()
