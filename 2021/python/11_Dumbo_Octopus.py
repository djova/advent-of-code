#!/usr/bin/env python3
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '11.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""


def parse(raw):
    return [[int(i) for i in s.strip()] for s in raw.split("\n") if s.strip()]


STEPS = [-1, 0, 1]


def neighbors(grid, x, y):
    xmax, ymax = len(grid[0]) - 1, len(grid) - 1
    for dx in STEPS:
        for dy in STEPS:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if nx > xmax or ny > ymax or nx < 0 or ny < 0:
                continue
            yield nx, ny


def printgrid(grid):
    print("\n".join("".join(str(i) for i in line) for line in grid))


def itergrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            yield x, y


def step(grid):
    flash_count = 0

    flashes = []
    for x, y in itergrid(grid):
        grid[y][x] += 1
        if grid[y][x] > 9:
            grid[y][x] = 0
            flashes.append((x, y))

    while flashes:
        fx, fy = flashes.pop()
        flash_count += 1
        for x, y in neighbors(grid, fx, fy):
            if grid[y][x] == 0:
                continue
            grid[y][x] += 1
            if grid[y][x] > 9:
                grid[y][x] = 0
                flashes.append((x, y))

    return flash_count


def go(grid, steps):
    total_flashes = 0
    for i in range(steps):
        # printgrid(grid)
        step_flashes = step(grid)
        # print(f"step {i} \t\t\tflashes {step_flashes}")
        if step_flashes == 100:
            print(f"all flashed at step: {i + 1}")
            break
        if i % 100 == 0:
            print("step ", i)
        total_flashes += step_flashes

    return f"total flashes: {total_flashes}"


# print(go(parse(test_input1), 100))
# print(go(parse(test_input1), 200))
print(go(parse(raw_input), 1000))
