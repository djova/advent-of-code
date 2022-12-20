#!/usr/bin/env python3
import re
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()

test_input = """\
30373
25512
65332
33549
35390
"""


def parse_grid(raw_input):
    lines = [s.strip() for s in raw_input.split('\n') if s.strip()]
    return [[int(c) for c in l] for l in lines]


def count_visible(grid, reverse_inner=False, reverse_outer=False, swap_outer_inner=False):
    n_rows, n_cols = len(grid), len(grid[0])
    visible = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    outer = range(n_rows)
    inner = range(n_cols)

    if reverse_inner:
        inner = list(reversed(inner))

    if reverse_outer:
        outer = list(reversed(outer))

    if swap_outer_inner:
        inner, outer = outer, inner

    for i in outer:
        max_height = -1
        for j in inner:
            t = grid[j][i] if swap_outer_inner else grid[i][j]
            if t > max_height:
                vi, vj = (j, i) if swap_outer_inner else (i, j)
                visible[vi][vj] = 1
                max_height = t

    return visible


def count_non_zero(grid):
    result = 0
    for row in grid:
        for x in row:
            if x > 0:
                result += 1
    return result


def merge_grids(grids):
    n_rows, n_cols = len(grids[0]), len(grids[0][0])
    result = [[0 for _ in range(n_cols)] for _ in range(n_rows)]
    for g in grids:
        for i in range(n_rows):
            for j in range(n_cols):
                result[i][j] += g[i][j]
    return result


def part1(raw_input):
    grid = parse_grid(raw_input)

    left = count_visible(grid)
    right = count_visible(grid, reverse_inner=True)
    top = count_visible(grid, swap_outer_inner=True)
    bottom = count_visible(grid, reverse_outer=True, swap_outer_inner=True)
    merged = merge_grids([left, right, top, bottom])
    return count_non_zero(merged)


def part2(raw_input):
    return 0


def test_visible_left():
    grid = parse_grid(test_input)
    expected = """\
    10010
    11000
    10000
    10101
    11010
    """
    left = count_visible(grid)
    expected = parse_grid(expected)
    assert left == expected, "left"


def test_visible_right():
    grid = parse_grid(test_input)

    expected = """\
    00011
    00101
    11011
    00001
    00011
    """
    right = count_visible(grid, reverse_inner=True)
    expected = parse_grid(expected)
    assert right == expected, "right"


def test_visible_top():
    grid = parse_grid(test_input)
    expected = """\
    11111
    01100
    10000
    00001
    00010
    """

    top = count_visible(grid, swap_outer_inner=True)
    expected = parse_grid(expected)
    assert top == expected, "top"


def test_visible_bottom():
    grid = parse_grid(test_input)
    expected = """\
    00000
    00000
    10000
    00101
    11111
    """

    bottom = count_visible(grid, swap_outer_inner=True, reverse_outer=True)
    expected = parse_grid(expected)
    assert bottom == expected, "bottom"


def test_part1():
    assert part1(test_input) == 21


def test_visible_trees_left():
    grid = parse_grid(test_input)
    expected = """\
    01231
    01112
    01111
    01112
    01121
    """
    left = count_visible(grid)
    expected = parse_grid(expected)
    assert left == expected, "left"


def test_part2():
    assert part2(test_input) == 24933642


if __name__ == '__main__':
    print("Part 1: ", part1(input_text))
    # print("Part 2: ", part2(input_text))
