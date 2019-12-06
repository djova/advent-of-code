#!/usr/bin/env python3
import math
from os.path import join, dirname, realpath

from lib.intcode import runcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '03.txt')
input_wires = [l.strip().split(',') for l in open(input_file, 'r').readlines()]

test_wires_1 = [
    "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(','),
    "U62,R66,U55,R34,D71,R55,D58,R83".split(',')
]
test_wires_2 = [
    "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(','),
    "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')
]

directions = {
    'U': (0, 1),
    'R': (1, 0),
    'L': (-1, 0),
    'D': (0, -1)
}


def nav_wire(wire):
    x, y = 0, 0
    for turn in wire:
        d, steps = turn[0], int(turn[1:])
        dx, dy = directions[d]
        for _ in range(steps):
            x += dx
            y += dy
            yield x, y


def run_wires(wires):
    wire_coordinates = {}
    for i, wire in enumerate(wires):
        wire_coordinates[i] = list(nav_wire(wire))

    intersections = set(wire_coordinates[0]).intersection(set(wire_coordinates[1]))

    def manhattan_distance(p):
        x, y = p
        return abs(x + y)

    smallest_1 = min(intersections, key=manhattan_distance)

    print(manhattan_distance(smallest_1))

    def summed_steps(p):
        return wire_coordinates[0].index(p) + wire_coordinates[1].index(p) + 2

    smallest_2 = min(intersections, key=summed_steps)
    print(summed_steps(smallest_2))


run_wires(input_wires)
