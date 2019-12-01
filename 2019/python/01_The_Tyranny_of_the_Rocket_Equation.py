#!/usr/bin/env python3
import math
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '01.txt')
input_ints = [int(l.strip()) for l in open(input_file, 'r').readlines()]


def fuel_required(mass):
    return math.floor(mass / 3) - 2


print("Part 1:", sum([fuel_required(m) for m in input_ints]))


def total_fuel_required(fuel):
    total = 0
    while (fuel := fuel_required(fuel)) > 0:
        total += fuel
    return total


print("Part 2:", sum([total_fuel_required(m) for m in input_ints]))
