#!/usr/bin/env python3
import functools
import math
import re
from collections import defaultdict
from os.path import join, dirname, realpath

import pytest

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '05.txt')
input_text = open(input_file, 'r').read()


def parse_raw_input(raw_input):
    lines = [l.strip() for l in raw_input.split('\n') if l.strip()]
    sections = []
    ranges = []
    for l in lines:
        if l.startswith('seeds:'):
            sections.append([int(d) for d in re.findall('\d+', l)])
            continue
        if not l[0].isdigit():
            if ranges:
                sections.append(ranges)
            ranges = []
            continue
        ranges.append([int(d) for d in re.findall('\d+', l)])
    if ranges:
        sections.append(ranges)
    return sections


test_input = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def get_lowest_location(raw_input):
    sections = parse_raw_input(raw_input)
    values = sections[0]
    for i, ranges in enumerate(sections[1:]):
        ranges = sorted(ranges, key=lambda r: r[1], reverse=True)
        new_values = []
        for v in values:
            for dest, start, length in ranges:
                if start <= v < start + length:
                    new_v = v + dest - start
                    new_values.append(new_v)
                    break
            else:
                new_values.append(v)
        values = new_values
    return min(values)


"""

------
   -------
   
   -------
-------
   
"""


def get_overlap(v_start, v_end, r_start, r_end):
    if v_start <= r_start < v_end:
        return r_start, min(v_end, r_end)
    if r_start <= v_start < r_end:
        return v_start, min(v_end, r_end)
    return None, None


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_lowest_location_part_2(raw_input, values_override=None):
    sections = parse_raw_input(raw_input)
    orig_seeds = sections[0] if not values_override else values_override
    values = [(v, v + l - 1) for v, l in chunks(orig_seeds, 2)]
    for i, ranges in enumerate(sections[1:]):
        ranges = sorted(ranges, key=lambda r: r[1], reverse=True)
        new_values = []
        for v_start, v_end in values:
            mapped = False
            for r_dest, r_start, r_length in ranges:
                o_start, o_end = get_overlap(v_start, v_end, r_start, r_end=r_start + r_length - 1)
                if not o_start and not o_end:
                    continue
                d_o = r_dest - r_start
                new_values.append((o_start + d_o, o_end + d_o))
                mapped = True
            if not mapped:
                new_values.append((v_start, v_end))
        values = new_values
    return min([start for start, end in values])


def test_lowest_location():
    assert get_lowest_location(test_input) == 35


def test_lowest_location_part_2():
    assert get_lowest_location_part_2(test_input, values_override=[82, 1]) == 46


def run_main():
    print("part 1:", get_lowest_location(input_text))
    print("part 2:", get_lowest_location_part_2(input_text))


if __name__ == '__main__':
    run_main()
