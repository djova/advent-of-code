#!/usr/bin/env python3
import math
from collections import defaultdict
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '11.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().split(',')]

# (0, 0) is top left
UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)

TURN_LEFT = 0
TURN_RIGHT = 1


def turn_dir(current_dir, turn_dir):
    dx, dy = current_dir
    if turn_dir == TURN_LEFT:
        return dy, -dx
    elif turn_dir == TURN_RIGHT:
        return -dy, dx
    else:
        raise Exception("unknown turn dir")


def run_tests():
    assert turn_dir(UP, TURN_LEFT) == LEFT
    assert turn_dir(LEFT, TURN_LEFT) == DOWN
    assert turn_dir(DOWN, TURN_LEFT) == RIGHT
    assert turn_dir(RIGHT, TURN_LEFT) == UP
    assert turn_dir(UP, TURN_RIGHT) == RIGHT
    assert turn_dir(RIGHT, TURN_RIGHT) == DOWN
    assert turn_dir(DOWN, TURN_RIGHT) == LEFT
    assert turn_dir(LEFT, TURN_RIGHT) == UP


def move_point(p, d):
    px, py = p
    dx, dy = d
    return px + dx, py + dy


def paint(start_color):
    p = (0, 0)
    d = UP
    grid = {}
    ic = Intcode(input_ints)
    while True:
        color = grid.get(p, 0) if grid else start_color
        ic.add_input(color)
        outputs = list(ic.run_safe())
        if not outputs:
            break
        color, turn = outputs
        grid[p] = color
        d = turn_dir(d, turn)
        p = move_point(p, d)
    return grid


def render_grid(grid):
    points = grid.keys()
    min_x, min_y = min(p[0] for p in points), min(p[1] for p in points)
    max_x, max_y = max(p[0] for p in points), max(p[1] for p in points)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            p = (x, y)
            color = grid.get(p, 0)
            c = '.' if color == 0 else '#'
            print(c, end='')
        print()


run_tests()
p1 = paint(0)
print(len(p1))

p2 = paint(1)
render_grid(p2)
