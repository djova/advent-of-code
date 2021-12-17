#!/usr/bin/env python3
from os.path import join, dirname, realpath

import heapq
from builtins import int

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '15.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def parse(raw):
    return [[int(c) for c in l.strip()] for l in raw.split("\n") if l.strip()]


def itergrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            yield x, y


def neighbors(grid, x, y):
    xmax, ymax = len(grid[0]) - 1, len(grid) - 1
    for dx, dy in [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    ]:
        nx, ny = x + dx, y + dy
        if nx > xmax or ny > ymax:
            continue
        if ny < 0 or nx < 0:
            continue
        yield nx, ny


def printcost(cost, raw=False):
    if raw:
        print("\n".join(" ".join(["0" + str(c) if c < 10 else str(c) for c in row]) for row in cost))
        return
    max_val = max([cost[y][x] for x, y in itergrid(cost)])
    for x, y in itergrid(cost):
        cost[y][x] = cost[y][x] / max_val
    print("\n".join(" ".join(["{:.2f}".format(c) for c in row]) for row in cost))


def expand_grid(grid, times=5):
    grows, gcols = len(grid), len(grid[0])
    nrows, ncols = len(grid) * times, len(grid[0]) * times
    result = [[0 for _ in range(ncols)] for _ in range(nrows)]
    for mx in range(times):
        for my in range(times):
            for x, y in itergrid(grid):
                nx, ny = x + mx * grows, y + my * gcols
                result[nx][ny] = grid[y][x] + mx + my
                if result[nx][ny] > 9:
                    result[nx][ny] = (result[nx][ny] % 10) + 1
    return result


def incr_grid(grid):
    return [[i + 1 if i < 9 else 1 for i in row] for row in grid]


def go(grid):
    # dijkstra
    xmax, ymax = len(grid[0]) - 1, len(grid) - 1
    infty_cost = (xmax + 1) * (ymax + 1) * 9
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    cost = [[infty_cost for _ in range(len(grid[0]))] for _ in range(len(grid))]
    cost[0][0] = 0
    pending = []
    heapq.heappush(pending, (0, (0, 0)))
    while pending:
        _, (x, y) = heapq.heappop(pending)
        if visited[y][x]:
            continue
        for nx, ny in neighbors(grid, x, y):
            if visited[ny][nx]:
                continue
            nc = grid[ny][nx] + cost[y][x]
            if nc < cost[ny][nx]:
                cost[ny][nx] = nc
                heapq.heappush(pending, (nc, (nx, ny)))
                continue
        visited[y][x] = True

    return f"lowest cost: {cost[ymax][xmax]}"


print("test", go(parse(test_input1)))
print("part 1", go(parse(raw_input)))
print("part 2", go(expand_grid(parse(raw_input), 5)))
