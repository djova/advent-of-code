#!/usr/bin/env python3
import re
from collections import defaultdict
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()


def find_first_n_distinct(raw_input, n=4):
    raw_input = raw_input.strip()
    chars = defaultdict(int)
    # abcdefg
    for i in range(len(raw_input)):
        c = raw_input[i]
        chars[c] += 1
        if i < (n - 1):
            continue
        if len(chars) == n:
            return i + 1

        # drop last
        drop_c = raw_input[i - (n - 1)]
        chars[drop_c] -= 1
        if chars[drop_c] == 0:
            del chars[drop_c]
    raise Exception("invalid string")


def part2(raw_input):
    return 0


def test_part1():
    assert find_first_n_distinct("mjqjpqmgbljsphdztnvjfqwrcgsmlb", n=4) == 7
    assert find_first_n_distinct("bvwbjplbgvbhsrlpgdmjqwftvncz", n=4) == 5
    assert find_first_n_distinct("nppdvjthqldpwncqszvftbrmjlhg", n=4) == 6
    assert find_first_n_distinct("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", n=4) == 11


def test_part2():
    assert find_first_n_distinct("mjqjpqmgbljsphdztnvjfqwrcgsmlb", n=14) == 19
    assert find_first_n_distinct("bvwbjplbgvbhsrlpgdmjqwftvncz", n=14) == 23
    assert find_first_n_distinct("nppdvjthqldpwncqszvftbrmjlhg", n=14) == 23
    assert find_first_n_distinct("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", n=14) == 29
    assert find_first_n_distinct("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", n=14) == 26


print("Part 1: ", find_first_n_distinct(input_text, n=4))
print("Part 2: ", find_first_n_distinct(input_text, n=14))
