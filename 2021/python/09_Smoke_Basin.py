#!/usr/bin/env python3
from collections import Counter
from os.path import join, dirname, realpath

import math

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '09.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
2199943210
3987894921
9856789892
8767896789
9899965678
"""


def parse(raw):
    return [[int(s.strip()) for s in line.strip()] for line in raw.split("\n") if line.strip()]


def next_non_visited(visited):
    for x, y in itergrid(visited):
        if not visited[y][x]:
            return x, y
    return None


def itergrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            yield x, y


def neighbors(grid, x, y):
    xmax, ymax = len(grid[0]) - 1, len(grid) - 1
    for nx, ny in [
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
        (x, y - 1),
    ]:
        if nx < 0 or ny < 0 or nx > xmax or ny > ymax:
            continue
        yield nx, ny


def is_low_point(grid, x, y):
    h = grid[y][x]
    if h == 9:
        return False
    for nx, ny in neighbors(grid, x, y):
        if grid[ny][nx] < h:
            return False
    return True


def descend(grid, basins, start):
    x, y = start
    steps = []
    while True:
        steps.append((x, y))

        for nx, ny in neighbors(grid, x, y):
            # no backtrack
            if len(steps) > 1 and (nx, ny) == steps[-2]:
                continue

            # downhill or flat only
            if grid[ny][nx] >= grid[y][x]:
                continue

            x, y = nx, ny
            break
        else:
            break

    if is_low_point(grid, x, y):
        basins[y][x] = (x, y)

    if b := basins[y][x]:
        for sx, sy in steps:
            if grid[sy][sx] < 9:
                basins[sy][sx] = b
        return steps

    return steps


def find_risk(grid):
    basins = [[None for _ in range(len(grid[0]))] for _ in range(len(grid))]
    remaining = set(list(itergrid(grid)))

    while remaining:
        steps = descend(grid, basins, remaining.pop())
        remaining = remaining - set(steps)

    basin_sizes = Counter([basins[y][x] for x, y in itergrid(basins) if basins[y][x]])
    top_sizes = sorted(basin_sizes.values(), reverse=True)
    total_risk = sum([grid[y][x] + 1 for x, y in basin_sizes.keys()])
    basin_product = math.prod(top_sizes[0:3])

    return f"risk {total_risk}, basin product {basin_product}"


print("Basins (test): ", find_risk(parse(test_input1)))
print("Basins: ", find_risk(parse(raw_input)))
