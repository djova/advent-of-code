#!/usr/bin/env python3
import functools
import itertools
import math
import re
from collections import Counter
from enum import Enum
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '09.txt')
input_text = open(input_file, 'r').read()


def parse_raw_input(raw_input):
    lines = [l.strip() for l in raw_input.split('\n') if l.strip()]
    return [[int(d) for d in re.findall('-?\d+', l)] for l in lines]


test_input = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def ddx(sequence):
    for i in range(len(sequence) - 1):
        yield sequence[i + 1] - sequence[i]
    return []


def predict_next_value(sequence):
    if sum(sequence) == 0:
        return 0
    return sequence[-1] + predict_next_value(list(ddx(sequence)))


def run_main():
    print("part 1:", sum([predict_next_value(s) for s in parse_raw_input(input_text)]))
    print("part 2:", sum([predict_next_value(list(reversed(s))) for s in parse_raw_input(input_text)]))


def test_predict_next_value():
    sequences = parse_raw_input(test_input)
    next_values = [predict_next_value(s) for s in sequences]
    assert next_values == [18, 28, 68]
    assert sum(next_values) == 114


def test_predict_next_value_reversed():
    reversed_sequences = [list(reversed(s)) for s in parse_raw_input(test_input)]
    next_values_reversed = [predict_next_value(s) for s in reversed_sequences]
    assert next_values_reversed == [-3, 0, 5]


if __name__ == '__main__':
    run_main()
