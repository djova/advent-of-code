#!/usr/bin/env python3
import math
from os.path import join, dirname, realpath

from lib.intcode import runcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '02.txt')
input_ints = [int(l.strip()) for l in open(input_file, 'r').read().split(',')]

codes = input_ints.copy()
codes[1], codes[2] = 12, 2
print("Part 1:", runcode(codes)[0])


def search(target):
    for noun in range(0, 100):
        for verb in range(0, 100):
            codes = input_ints.copy()
            codes[1], codes[2] = noun, verb
            output = runcode(codes)
            if output[0] == target:
                return 100 * noun + verb
    raise Exception("no solution")


print("Part 2:", search(19690720))
