#!/usr/bin/env python3
import math
from collections import defaultdict, Counter
from os.path import join, dirname, realpath

import itertools
import re

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '20.txt')
raw_input = open(input_file, 'r').read()

test_input = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""


def parse(raw):
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    algo = lines[0]
    image = [list(l) for l in lines[1:]]
    return image, algo


def print_image(image):
    print("\n".join(''.join(row) for row in image))


def pad_image(image, pad_char, pad_size=3):
    # TODO: pad only as much as necessary
    print(f"padding image with '{pad_char}'")
    rows, cols = len(image), len(image[0])
    nros, ncols = rows + pad_size * 2, cols + pad_size * 2
    colpad = list(pad_char * pad_size)
    result = []
    for _ in range(pad_size):
        result.append(list(pad_char * ncols))
    for row in image:
        result.append(colpad + row + colpad)
    for _ in range(pad_size):
        result.append(list(pad_char * ncols))
    return result


def empty_copy(image, pad_char):
    return [list(pad_char * len(image[0])) for _ in range(len(image))]


def binary_s_to_int(raw):
    result = 0
    for i, c in enumerate(reversed(raw)):
        if c == '1':
            result += 2 ** i
    return result


def apply_algo(image, algo, x, y, pad_char):
    result_binary = ""
    for ay in [y - 1, y, y + 1]:
        for ax in [x - 1, x, x + 1]:
            out_of_bounds = ay < 0 or ax < 0 or ay > len(image) - 1 or ax > len(image[0]) - 1
            c = pad_char if out_of_bounds else image[ay][ax]
            result_binary += '0' if c == '.' else '1'

    ai = binary_s_to_int(result_binary)
    return algo[ai]


def enhance(image, algo, pad_char):
    result = empty_copy(image, pad_char)
    for y in range(0, len(image)):
        for x in range(len(image[0])):
            result[y][x] = apply_algo(image, algo, x, y, pad_char)
    return result


def enhance_pad_char(algo, pad_char):
    image = [[pad_char]]
    image = apply_algo(image, algo, 0, 0, pad_char)
    return image[0][0]


def need_to_pad(image):
    if len(set(itertools.chain(*image[0:3], *image[-3:]))) > 1:
        return True
    for row in image:
        if len(set(itertools.chain(*row[0:3], *row[-3:]))) > 1:
            return True

    return False


def enhance_times(image, algo, times):
    print_image(image)

    pad_char = '.'
    print(f"starting enhancements total={times} pad_char='{pad_char}'")

    for i in range(times):
        if need_to_pad(image):
            image = pad_image(image, pad_char)
        print_image(image)
        image = enhance(image, algo, pad_char)
        pad_char = enhance_pad_char(algo, pad_char)
        print(f"enhancement done i={i}")

    print("enhancements done")
    print_image(image)
    print(f"counts: {Counter(itertools.chain(*image))}")


print("running test")
enhance_times(*parse(test_input), 2)
# too high: 6319
print("running part 1")
enhance_times(*parse(raw_input), 2)
print("running part 2")
enhance_times(*parse(raw_input), 50)
