#!/usr/bin/env python3
import re
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '17.txt')
raw_input = open(input_file, 'r').read()

test_input = "target area: x=20..30, y=-10..-5"


def parse(raw):
    x1, x2, y1, y2 = [int(x) for x in re.findall(r"-?\d+", raw)]
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return x1, x2, y1, y2


def sort_pair(a, b):
    return (a, b) if a < b else (b, a)


def eval_steps(dx, dy, target_area):
    x1, x2, y1, y2 = target_area
    x, y = 0, 0
    max_y = 0
    success = False
    while True:
        if y > max_y:
            max_y = y
        if x > x2 or y < y1:
            break
        if x1 <= x <= x2 and y1 <= y <= y2:
            success = True
            break
        x += dx
        y += dy
        if dx != 0:
            dx = dx + 1 if dx < 0 else dx - 1
        dy -= 1
    return success, max_y


def go(target_area):
    x1, x2, y1, y2 = target_area
    max_y, max_v = 0, (0, 0)
    num_success = 0
    for dx in range(0, x2*2):
        for dy in range(y1, 400):
            success, my = eval_steps(dx, dy, target_area)
            if success:
                num_success += 1
                if my > max_y:
                    max_y, max_v = my, (dx, dy)

    return f"max_y={max_y} max_v={max_v} num_success={num_success}"


print("test: ", go(parse(test_input)))
print("part 1: ", go(parse(raw_input)))
