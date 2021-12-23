#!/usr/bin/env python3
from os.path import join, dirname, realpath

import functools
import itertools
import re

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '22.txt')
raw_input = open(input_file, 'r').read()

test_input_1 = """\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""

test_input_2 = """\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def parse(raw):
    lines = [re.findall(r"on|off|-?\d+", l) for l in raw.split("\n") if l.strip()]
    lines = [(l[0] == 'on', list(chunks([int(i) for i in l[1:]], 2))) for l in lines]
    return lines


def dim_overlap(da, db):
    a1, a2 = da
    b1, b2 = db
    if a1 <= b1 <= a2:
        return b1, min(b2, a2)
    if b1 <= a1 <= b2:
        return a1, min(a2, b2)
    return None


def split_overlap(da, db):
    a1, a2 = da
    b1, b2 = db
    if b1 > a1:
        yield a1, max(a1, b1 - 1)
    yield b1, b2
    if b2 < a2:
        yield min(b2 + 1, a2), a2


def region_overlap(ra, rb):
    ol = [dim_overlap(da, db) for da, db in zip(ra, rb)]
    return ol if all(ol) else None


def remove_region(orig, removal, axis=0):
    if not region_overlap(orig, removal):
        return [orig]
    if axis > len(removal) - 1:
        return []
    result = []
    od, rd = orig[axis], removal[axis]
    for d_rem in split_overlap(od, rd):
        n_region = orig[:]
        n_region[axis] = d_rem
        result.extend(remove_region(n_region, removal, axis + 1))
    return result


def remove_region_from_set(regions, removal):
    remainder = []
    for r in regions:
        ol = region_overlap(r, removal)
        if not ol:
            remainder.append(r)
            continue
        rem = remove_region(r, ol)
        remainder.extend(rem)
    return remainder


def total_area(regions):
    total = 0
    for r in regions:
        diffs = [b - a + 1 for a, b in r]
        area = functools.reduce(lambda a, b: a * b, diffs)
        total += area
    return total


def go(lines, ignore_range=None):
    on_regions = []
    for on, new_r in lines:
        if ignore_range:
            invalid_dims = [i for i in itertools.chain(*new_r) if not (- ignore_range <= i <= ignore_range)]
            if invalid_dims:
                print("ignoring as its outside range", new_r)
                continue
        print(f"processing line. on={on}: {new_r}")
        if on and not on_regions:
            on_regions.append(new_r)
            print(f"turning on net new lights: {total_area([new_r])}")
            continue
        if on:
            new_on_regions = [new_r]
            for on_r in on_regions:
                new_on_regions = remove_region_from_set(new_on_regions, on_r)
            print(f"turning ON net new lights: {total_area(new_on_regions)}")
            on_regions.extend(new_on_regions)
        else:
            new_on_regions = remove_region_from_set(on_regions, new_r)
            print(f"turning OFF net lights: {total_area(on_regions) - total_area(new_on_regions)}")
            on_regions = new_on_regions

    return total_area(on_regions)


def test_split_overlap():
    test_cases = [
        [
            ((0, 2), (1, 2)),
            ((0, 0), (1, 2)),
        ],
        [
            ((0, 2), (0, 1)),
            ((0, 1), (2, 2)),
        ],
        [
            ((0, 2), (1, 1)),
            ((0, 0), (1, 1), (2, 2)),
        ]
    ]
    for test_case, expected in test_cases:
        result = tuple(split_overlap(*test_case))
        print(f"result={result} expected={expected} success={result == expected}")


def test_basic_region_removal():
    print("test_basic_region_removal")
    orig = [(1, 3), (1, 3)]
    print("orig_size", total_area([orig]))
    removal = [(1, 2), (1, 2)]
    result = remove_region(orig, removal)
    print("result_size", total_area(result))

    print("test_basic_region_removal with negative")
    orig = [(-1, 1), (-1, 1)]
    print("orig_size", total_area([orig]))
    removal = [(-1, 0), (-1, 0)]
    result = remove_region(orig, removal)
    print("result_size", total_area(result))

    print("test_basic_region_removal middle")
    orig = [(-1, 1), (-1, 1)]
    print("orig_size", total_area([orig]))
    removal = [(1, 1), (1, 1)]
    result = remove_region(orig, removal)
    print("result_size", total_area(result))


# test_split_overlap()
# test_basic_region_removal()
# print("part1 test. total_area", go(parse(test_input_1)))
# print("part1 test. total_area", go(parse(test_input_2), ignore_range=50))
print("part1. total_area", go(parse(raw_input)))
# 406570 too low
