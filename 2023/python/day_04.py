#!/usr/bin/env python3
import functools
import math
import re
from collections import defaultdict
from os.path import join, dirname, realpath

import pytest

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '04.txt')
input_text = open(input_file, 'r').read()


def parse_raw_input(raw_input):
    lines = [l.strip() for l in raw_input.split('\n') if l.strip()]
    for l in lines:
        parsed = [[int(d) for d in re.findall('\d+', p)] for p in l.split('|')]
        yield parsed[0][0], parsed[0][1:], parsed[1]


test_input = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def total_points(raw_input):
    total = 0
    for card_n, winning_numbers, numbers in parse_raw_input(raw_input):
        n_winning = len(set(winning_numbers).intersection(set(numbers)))
        points = int(math.pow(2, n_winning - 1)) if n_winning > 0 else 0
        total += points
    return total


def total_scratchpads(raw_input):
    win_counts = defaultdict(int)
    for c, winning_numbers, numbers in parse_raw_input(raw_input):
        n = len(set(winning_numbers).intersection(set(numbers)))
        win_counts[c] += 1
        for i in range(1, n + 1):
            win_counts[c + i] += win_counts[c]

    return sum(win_counts.values())


def test_total_points():
    assert total_points(test_input) == 13


def test_total_scratchpads():
    assert total_scratchpads(test_input) == 30


def run_main():
    print("part 1:", total_points(input_text))
    print("part 2:", total_scratchpads(input_text))


if __name__ == '__main__':
    run_main()
