#!/usr/bin/env python3
import re
from collections import defaultdict, Counter
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '13.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


def parse(raw):
    coords, folds = [], []
    for l in raw.split("\n"):
        l = l.strip()
        if not l:
            continue
        ints = [int(i) for i in re.findall(r"\d+", l)]
        if len(ints) == 2:
            coords.append(ints)
            continue
        axis = l.split("=")[0][-1]
        folds.append((axis, ints[0]))

    return coords, folds


def to_grid(coords):
    xmax = max([x for x, _ in coords])
    ymax = max([y for _, y in coords])
    grid = [[False for _ in range(xmax + 1)] for _ in range(ymax + 1)]
    for x, y in coords:
        grid[y][x] = True
    return grid


def print_grid(grid):
    def _to_char(x):
        return '#' if x else '.'

    print("\n".join("".join([_to_char(x) for x in row]) for row in grid))


def count_dots(grid):
    return sum([sum(row) for row in grid])


def split(grid, axis, index):
    if axis == 'y':
        return grid[0:index], grid[index + 1:]
    else:
        grid_a = [r[0:index] for r in grid]
        grid_b = [r[index + 1:] for r in grid]
        return grid_a, grid_b


def iter_pairs_inward(length):
    max_i = length - 1
    mid_i = int(length / 2)
    if length % 2 == 0:
        mid_i -= 1
    for i in range(mid_i):
        j = max_i - i
        yield i, j


def flip(grid, axis):
    if axis == 'y':
        for y1, y2 in iter_pairs_inward(len(grid)):
            for x in range(len(grid[0])):
                grid[y1][x], grid[y2][x] = grid[y2][x], grid[y1][x]
    else:
        for x1, x2 in iter_pairs_inward(len(grid[0])):
            for y in range(len(grid)):
                grid[y][x1], grid[y][x2] = grid[y][x2], grid[y][x1]
    return grid


def combine(a, b):
    dy = len(a) - len(b)
    dx = len(a[0]) - len(b[0])

    if dy < 0 or dx < 0:
        raise Exception("handle negative fold")

    if dy > 0 or dx > 0:
        hello = 5

    for by in range(len(b)):
        for bx in range(len(b[0])):
            ay, ax = by + dy, bx + dx
            a[ay][ax] = any([a[ay][ax], b[by][bx]])

    return a


def fold(grid, axis, index):
    a, b = split(grid, axis, index)
    flip(b, axis)
    a = combine(a, b)
    return a


def do_folds(coords, folds, debug=False):
    grid = to_grid(coords)
    print("starting folds")
    if debug:
        print_grid(grid)
    for i, (axis, index) in enumerate(folds):
        prex, prey = len(grid[0]), len(grid)
        grid = fold(grid, axis, index)
        postx, posty = len(grid[0]), len(grid)
        print(f"fold={i + 1} axis={axis} index={index} dim-before={(prex, prey)} dim-after={(postx, posty)} dots={count_dots(grid)}")
        if debug:
            print_grid(grid)

    print("folds complete")
    print_grid(grid)


def do_folds_alternate(coords, folds, debug=False):
    print("starting folds")
    coords = set(tuple((x, y) for x, y in coords))
    print_grid(to_grid(coords))
    for i, (axis, index) in enumerate(folds):
        new_coords = set()
        # apply fold
        for x, y in coords:
            if axis == 'x':
                if x < index:
                    new_coords.add((x, y))
                    continue
                if x == index:
                    # lost on fold. shouldn't happen
                    continue
                x = x - 2 * (x - index)
                new_coords.add((x, y))
            else:
                if y < index:
                    new_coords.add((x, y))
                    continue
                if y == index:
                    # lost on fold. shouldn't happen
                    continue
                new_y = y - 2 * (y - index)
                new_coords.add((x, new_y))
        prex, prey = max([y for x, y in coords]), max([x for x, y in coords])
        postx, posty = max([y for x, y in new_coords]), max([x for x, y in new_coords])
        print(f"fold={i + 1} axis={axis} index={index} dim-before={(prex, prey)} dim-after={(postx, posty)} dots={len(new_coords)}")
        coords = new_coords
        if debug:
            print_grid(to_grid(coords))

    print_grid(to_grid(coords))


print("test", do_folds_alternate(*parse(test_input1), debug=True))

print("part 1", do_folds_alternate(*parse(raw_input)))
