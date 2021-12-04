#!/usr/bin/env python3
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '03.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def parse(raw):
    return [[int(x) for x in list(s)] for s in raw.split("\n") if s.strip()]


def bits_to_decimal(bits):
    res = 0
    for i, bit in enumerate(reversed(bits)):
        if bit:
            res += 2 ** i
    return res


def part_1(raw):
    numbers = parse(raw)
    bits = [round(sum(column) / len(numbers)) for column in zip(*numbers)]
    g = bits_to_decimal(bits)
    e = bits_to_decimal([0 if i == 1 else 1 for i in bits])
    return {
        "gamma_rate": g,
        "epsilon_rate": e,
        "mul": g * e,
    }


print("Part 1 (test): ", part_1(test_input1))
print("Part 1: ", part_1(raw_input))


def reduce_bits(numbers, keep_most_common):
    bitlen = len(numbers[0])
    bit = 0
    while bit < bitlen and len(numbers) > 1:
        columns = list(zip(*numbers))
        f = sum(columns[bit]) / len(numbers)
        keep_bit = 1 if f == 0.5 else round(f)
        if not keep_most_common:
            keep_bit = 0 if keep_bit == 1 else 1
        numbers = [n for n in numbers if n[bit] == keep_bit]
        bit += 1
    return numbers[0]


def part_2(raw):
    numbers = parse(raw)
    o2 = bits_to_decimal(reduce_bits(numbers, True))
    co2 = bits_to_decimal(reduce_bits(numbers, False))
    return {
        "02-gen": o2,
        "c02-scrub": co2,
        "mul": o2 * co2,
    }


print("Part 2 (test): ", part_2(test_input1))
print("Part 2: ", part_2(raw_input))
