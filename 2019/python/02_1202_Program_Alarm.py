#!/usr/bin/env python3
import math
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '02.txt')
input_ints = [int(l.strip()) for l in open(input_file, 'r').read().split(',')]


def evaluate(codes):
    i = 0
    while codes[i] != 99:
        opcode, a, b, c = codes[i:i + 4]
        if opcode == 1:
            codes[c] = codes[a] + codes[b]
        elif opcode == 2:
            codes[c] = codes[a] * codes[b]
        else:
            raise Exception("unknown code")
        i += 4
    return codes


codes = input_ints.copy()
codes[1], codes[2] = 12, 2
print("Part 1:", evaluate(codes)[0])


def search_inputs(target):
    for noun in range(0, 100):
        for verb in range(0, 100):
            codes = input_ints.copy()
            codes[1], codes[2] = noun, verb
            output = evaluate(codes)
            if output[0] == target:
                return 100 * noun + verb
    raise Exception("no solution")


print("Part 2:", search_inputs(19690720))
