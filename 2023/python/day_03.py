#!/usr/bin/env python3
import functools
import re
from collections import defaultdict
from os.path import join, dirname, realpath

import pytest

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '03.txt')
input_text = open(input_file, 'r').read()


def parse_raw_input(raw_input):
    lines = [l.strip() for l in raw_input.split('\n') if l.strip()]
    return lines


test_input = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def iter_grid(grid):
    max_y, max_x = len(grid), len(grid[0])
    for iy in range(max_y):
        for ix in range(max_x):
            yield (iy, ix), grid[iy][ix]


def find_symbol_locations(grid):
    for (iy, ix), c in iter_grid(grid):
        if not c.isdigit() and c != '.':
            yield (iy, ix), c


neighboring_steps = [-1, 0, 1]


def iter_neighbors(grid, iy, ix):
    for dy in neighboring_steps:
        next_y = dy + iy
        if next_y < 0 or next_y >= len(grid):
            continue
        for dx in neighboring_steps:
            next_x = dx + ix
            if next_x < 0 or next_x >= len(grid[0]):
                continue
            yield (next_y, next_x), grid[next_y][next_x]


def consume_horizontal_number(grid, iy, ix):
    a, b = ix, ix
    while a > 0:
        next_x = a - 1
        if grid[iy][next_x].isdigit():
            a = next_x
            continue
        break
    while b < len(grid[0]) - 1:
        next_x = b + 1
        if grid[iy][next_x].isdigit():
            b = next_x
            continue
        break
    coords = [(iy, x) for x in range(a, b + 1)]
    return coords, int(''.join([grid[y][x] for y, x in coords]))


def find_neighboring_part_numbers(grid, iy, ix):
    remaining_neighbors = set([(next_y, next_x) for (next_y, next_x), _ in iter_neighbors(grid, iy, ix)])
    while remaining_neighbors:
        (next_y, next_x) = remaining_neighbors.pop()
        c = grid[next_y][next_x]
        if c.isdigit():
            coordinates, number = consume_horizontal_number(grid, next_y, next_x)
            remaining_neighbors = remaining_neighbors.difference(set(coordinates))
            yield coordinates[0], number


def extract_part_numbers(grid):
    seen_number_indexes = set()
    for (iy, ix), c in find_symbol_locations(grid):
        for (piy, pix), part_number in find_neighboring_part_numbers(grid, iy, ix):
            if (piy, pix) not in seen_number_indexes:
                seen_number_indexes.add((piy, pix))
                yield part_number


def test_extract_part_numbers():
    grid = parse_raw_input(test_input)
    part_numbers = list(extract_part_numbers(grid))
    assert sum(part_numbers) == 4361


def extract_gear_ratios(grid):
    for (iy, ix), c in find_symbol_locations(grid):
        if c != '*':
            continue
        neighboring_part_numbers = [n for _, n in find_neighboring_part_numbers(grid, iy, ix)]
        if len(neighboring_part_numbers) == 2:
            yield neighboring_part_numbers[0] * neighboring_part_numbers[1]


def test_extract_gear_ratios():
    grid = parse_raw_input(test_input)
    assert sum(extract_gear_ratios(grid)) == 467835


def run_main():
    grid = parse_raw_input(input_text)
    print("part 1:", sum(extract_part_numbers(grid)))
    print("part 2:", sum(extract_gear_ratios(grid)))


if __name__ == '__main__':
    run_main()
