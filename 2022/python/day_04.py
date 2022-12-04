#!/usr/bin/env python3
import re
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()

test_input_text = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def process_raw_input(raw_input):
    for line in raw_input.split('\n'):
        line = line.strip()
        if not line:
            continue
        yield [int(d) for d in re.findall(r'\d+', line)]


def a_in_b(a1, a2, b1, b2):
    return b1 >= a1 and b2 <= a2


def part1(raw_input):
    result = 0
    for a1, a2, b1, b2 in process_raw_input(raw_input):
        if a_in_b(a1, a2, b1, b2):
            result += 1
        elif a_in_b(b1, b2, a1, a2):
            result += 1
    return result


def has_overlap(a1, a2, b1, b2):
    """
    a1    a2
        b1    b2

            a1    a2
        b1    b2
    """
    if a1 <= b1 <= a2:
        return True
    if b1 <= a1 <= b2:
        return True
    return False


def part2(raw_input):
    result = 0
    for a1, a2, b1, b2 in process_raw_input(raw_input):
        if has_overlap(a1, a2, b1, b2):
            result += 1
    return result


def test_part1():
    assert part1(test_input_text) == 2


def test_part2():
    assert part2(test_input_text) == 4


print("Part 1: ", part1(input_text))
print("Part 2: ", part2(input_text))
