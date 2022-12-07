#!/usr/bin/env python3
import re
from collections import defaultdict
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()


def part1(raw_input):
    raw_input = raw_input.strip()
    chars = defaultdict(int)
    # abcdefg
    for i in range(len(raw_input)):
        c = raw_input[i]
        chars[c] += 1
        if i < 3:
            continue
        if len(chars) == 4:
            return i + 1

        # drop last
        drop_c = raw_input[i - 3]
        chars[drop_c] -= 1
        if chars[drop_c] == 0:
            del chars[drop_c]
    raise Exception("invalid string")


def part2(raw_input):
    return 0


def test_part1():
    assert part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part1("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11


# def test_part2():
#     assert part2(inpu) == "MCD"


print("Part 1: ", part1(input_text))
# print("Part 2: ", part2(input_text))
