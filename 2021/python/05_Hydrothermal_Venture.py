#!/usr/bin/env python3
import time
from os.path import join, dirname, realpath
import re
import itertools

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '05.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def parse(raw):
    lines = []
    for line in raw.split("\n"):
        if not line.strip():
            continue
        lines.append([int(x) for x in re.findall(r"\d+", line)])

    return lines


def itergrid(grid):
    num_rows = len(grid)
    num_cols = len(grid[0])
    for y in range(num_rows):
        for x in range(num_cols):
            yield x, y


def printgrid(grid):
    fmtrows = []
    for row in grid:
        fmtrows.append("".join([str(i) for i in row]))
    print("\n".join(fmtrows).replace("0", "."))


def sort_coords(*args):
    return sorted(args)


def step(x1, y1, x2, y2):
    if x1 != x2:
        x1 += 1 if x2 > x1 else -1
    if y1 != y2:
        y1 += 1 if y2 > y1 else -1
    return x1, y1


def fill_grid(grid, lines, include_diagonal=False):
    for x1, y1, x2, y2 in lines:
        # is_flat = x1 == x2 or y1 == y2
        # if not is_flat and not include_diagonal:
        #     continue
        x3, y3 = x1, y1
        grid[x3][y3] += 1
        while (x3, y3) != (x2, y2):
            x3, y3 = step(x3, y3, x2, y2)
            grid[x3][y3] += 1

    return grid


def part_1(raw):
    lines = parse(raw)
    max_num = max(itertools.chain(*lines))
    grid = [[0 for _ in range(max_num + 1)] for _ in range(max_num + 1)]
    grid = fill_grid(grid, lines, include_diagonal=False)
    num_overlap = len([True for x, y in itergrid(grid) if grid[x][y] > 1])
    # printgrid(grid)
    return f"# points with > 2 overlap: {num_overlap}"


print("Part 1 (test): ", part_1(test_input1))
print("Part 1: ", part_1(raw_input))


def part_2(raw):
    lines = parse(raw)
    max_num = max(itertools.chain(*lines))
    grid = [[0 for _ in range(max_num + 1)] for _ in range(max_num + 1)]
    grid = fill_grid(grid, lines, include_diagonal=True)
    num_overlap = len([True for x, y in itergrid(grid) if grid[x][y] > 1])
    # printgrid(grid)
    return f"# points with > 2 overlap: {num_overlap}"


print("Part 2 (test): ", part_1(test_input1))
print("Part 2: ", part_1(raw_input))
