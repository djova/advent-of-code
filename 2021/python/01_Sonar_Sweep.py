#!/usr/bin/env python3
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '01.txt')
input_ints = [int(l.strip()) for l in open(input_file, 'r').readlines()]

prev = None
increases = 0
for m in input_ints:
    if not prev:
        prev = m
        continue
    if m > prev:
        increases += 1
    prev = m

print("Part 1:", increases)

test_input = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263
]


def part_2(measurements):
    last, increases = 0, 0
    for i in range(len(measurements) - 2):
        window = sum(measurements[i:i + 3])
        if not last:
            last = window
            continue
        if window > last:
            increases += 1
        last = window
    return increases


print("Test Part 2:", part_2(test_input), "expected", 5)
print("Part 2:", part_2(input_ints))
