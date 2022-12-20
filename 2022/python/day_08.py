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


def iter_rows(grid, reverse=False):
    n_rows, n_cols = len(grid), len(grid[0])
    for i in range(n_rows):
        cols = range(n_cols)
        if reverse:
            cols = reversed(cols)
        yield [(i, j) for j in cols]


def iter_cols(grid, reverse=False):
    n_rows, n_cols = len(grid), len(grid[0])
    for j in range(n_cols):
        rows = range(n_rows)
        if reverse:
            rows = reversed(rows)
        yield [(i, j) for i in rows]


def visible_from_edge(row):
    max_height = -1
    for x in row:
        if x > max_height:
            yield 1
            max_height = x
        else:
            yield 0


def visible_trees(row):
    row = list(row)
    for i in range(len(row)):
        count = 0
        for j in reversed(range(0, i)):
            count += 1
            if row[j] >= row[i]:
                break

        yield count


def count_non_zero(grid):
    result = 0
    for row in grid:
        for x in row:
            if x > 0:
                result += 1
    return result


def merge_grids(grids, merge_func):
    n_rows, n_cols = len(grids[0]), len(grids[0][0])
    result = grids[0]
    for g in grids[1:]:
        for i in range(n_rows):
            for j in range(n_cols):
                result[i][j] = merge_func(result[i][j], g[i][j])
    return result


def count_visible(grid, direction, vfunc):
    n_rows, n_cols = len(grid), len(grid[0])
    visible = [[0 for _ in range(n_cols)] for _ in range(n_rows)]

    if direction == "left":
        rows = iter_rows(grid)
    elif direction == "right":
        rows = iter_rows(grid, reverse=True)
    elif direction == "top":
        rows = iter_cols(grid)
    elif direction == "bottom":
        rows = iter_cols(grid, reverse=True)
    else:
        raise Exception("invalid")

    for row in rows:
        row_vals = [grid[i][j] for (i, j) in row]
        for (i, j), v in zip(row, vfunc(row_vals)):
            visible[i][j] = v

    return visible


sides = ["left", "right", "top", "bottom"]


def part1(raw_input):
    grid = parse_grid(raw_input)
    grids = [count_visible(grid, side, visible_from_edge) for side in sides]
    merged = merge_grids(grids, lambda a, b: a + b)
    return count_non_zero(merged)


def part2(raw_input):
    grid = parse_grid(raw_input)
    sides = ["left", "right", "top", "bottom"]
    grids = [count_visible(grid, side, visible_trees) for side in sides]
    merged = merge_grids(grids, lambda a, b: a * b)
    return max([max(row) for row in merged])


def test_visible_edge_left():
    grid = parse_grid(test_input)
    expected = """\
    10010
    11000
    10000
    10101
    11010
    """
    left = count_visible(grid, "left", visible_from_edge)
    expected = parse_grid(expected)
    assert left == expected, "left"


def test_visible_edge_right():
    grid = parse_grid(test_input)

    expected = """\
    00011
    00101
    11011
    00001
    00011
    """
    right = count_visible(grid, "right", visible_from_edge)
    expected = parse_grid(expected)
    assert right == expected, "right"


def test_visible_edge_top():
    grid = parse_grid(test_input)
    expected = """\
    11111
    01100
    10000
    00001
    00010
    """

    top = count_visible(grid, "top", visible_from_edge)
    expected = parse_grid(expected)
    assert top == expected, "top"


def test_visible_edge_bottom():
    grid = parse_grid(test_input)
    expected = """\
    00000
    00000
    10000
    00101
    11111
    """

    bottom = count_visible(grid, "bottom", visible_from_edge)
    expected = parse_grid(expected)
    assert bottom == expected, "bottom"


def test_part1():
    assert part1(test_input) == 21


def test_visible_trees_left():
    assert list(visible_trees([3, 0, 3, 7, 3])) == [0, 1, 2, 3, 1]
    assert list(visible_trees([2, 5, 5, 1, 2])) == [0, 1, 1, 1, 2]
    assert list(visible_trees([6, 5, 3, 3, 2])) == [0, 1, 1, 1, 1]
    assert list(visible_trees([3, 3, 5, 4, 9])) == [0, 1, 2, 1, 4]
    assert list(visible_trees([3, 5, 3, 9, 0])) == [0, 1, 1, 3, 1]


def test_part2():
    assert part2(test_input) == 8


if __name__ == '__main__':
    print("Part 1: ", part1(input_text))
    print("Part 2: ", part2(input_text))
