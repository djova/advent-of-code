#!/usr/bin/env python3
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '02.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


def parse(raw):
    r = [s.split(" ") for s in raw.split("\n") if s.strip()]
    return [(a, int(p)) for a, p in r]


def part_1(raw):
    actions = parse(raw)
    position, depth = 0, 0
    for action, X in actions:
        if action == "forward":
            position += X
        elif action == "up":
            depth -= X
        elif action == "down":
            depth += X
        else:
            raise Exception("invalid action: " + action)
    return {
        "position": position,
        "depth": depth,
        "mul": position * depth
    }


print("Part 1 (test): ", part_1(test_input1))
print("Part 1: ", part_1(raw_input))


def part_2(raw):
    actions = parse(raw)
    position, depth, aim = 0, 0, 0
    for action, X in actions:
        if action == "forward":
            position += X
            depth += aim * X
        elif action == "up":
            aim -= X
        elif action == "down":
            aim += X
        else:
            raise Exception("invalid action: " + action)
    return {
        "position": position,
        "depth": depth,
        "mul": position * depth
    }

print("Part 2 (test): ", part_2(test_input1))
print("Part 2: ", part_2(raw_input))
