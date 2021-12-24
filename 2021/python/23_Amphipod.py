#!/usr/bin/env python3
from collections import defaultdict
from os.path import join, dirname, realpath

import functools
import itertools
import re

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '23.txt')
raw_input = open(input_file, 'r').read()

test_input_1 = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

done_example = """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""


def parse(raw):
    grid = []
    width = None
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        if not width:
            width = len(line)
        if len(line) < width:
            pad_size = (width - len(line)) // 2
            line = '#' * pad_size + line + '#' * pad_size
        grid.append(list(line))

    return grid


a_costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

room_targets = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
}

desired_rooms = {v: k for k, v in room_targets.items()}

room_indexes = {
    0: ((3, 2), (3, 3)),
    1: ((5, 2), (5, 3)),
    2: ((7, 2), (7, 3)),
    3: ((9, 2), (9, 3)),
}


def print_grid(grid):
    print("\n" + "\n".join([''.join(row) for row in grid]) + "\n")


def itergrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            yield x, y


def is_done(grid):
    for r_i, rooms in room_indexes.items():
        target_a = room_targets[r_i]
        for x, y in rooms:
            if grid[y][x] != target_a:
                return False
    return True


def a_positions(grid):
    positions = defaultdict(list)
    for x, y in itergrid(grid):
        c = grid[y][x]
        if c in a_costs:
            positions[c].append((x, y))
    return positions


def ideal_move(grid, x, y):
    a = grid[y][x]
    if a not in a_costs:
        raise Exception("invalid")
    desired_positions = sorted(room_indexes[desired_rooms[a]], key=lambda p: p[1], reverse=True)
    for px, py in desired_positions:
        if (x, y) == (px, py):
            return None
        if grid[py][px] == a:
            continue
        return (x, y), (px, py)


def shortest_path(grid, from_p, to_p):
    x, y = from_p
    to_x, to_y = to_p
    while (x, y) != (to_x, to_y):
        dx, dy = to_x - x, to_y - y
        if dx == 0:
            y += 1 if dy > 0 else -1
        elif y == 1:
            # corridor
            x += 1 if dx > 0 else -1
        else:
            # another room
            y -= 1
        yield x, y


def next_blocking_pos(grid, from_p, to_p):
    to_x, to_y = to_p
    if grid[to_y][to_x] != '.':
        return to_x, to_y
    for x, y in shortest_path(grid, from_p, to_p):
        if grid[y][x] != '.':
            if grid[y][x] not in a_costs:
                raise Exception("invalid")
            return x, y
    return None


def do_move(grid, pending_moves, move_from, move_to):
    (from_x, from_y), (to_x, to_y) = move_from, move_to
    print(f"move {grid[from_y][from_x]}: {move_from} -> {move_to}")
    grid[to_y][to_x] = grid[from_y][from_x]
    grid[from_y][from_x] = '.'
    for i, (pend_from, pend_to) in enumerate(pending_moves):
        if pend_from == move_from:
            pending_moves[i] = (move_to, pend_to)


descending_cost_priority = [
    'D',
    'C',
    'B',
    'A',
]


def next_best_move(grid):
    a_pos = a_positions(grid)
    hallway_pos = [(x, y) for x, y in itertools.chain(*a_pos.values()) if y == 1]
    if hallway_pos:
        ideal_moves = [ideal_move(grid, x, y) for x, y in hallway_pos]
        ideal_moves = [m for m in ideal_moves if m]
        ideal_moves = sorted(ideal_moves, key=lambda p: len(list(shortest_path(grid, *p))))
        if ideal_moves:
            return ideal_moves[0]
    for a in descending_cost_priority:
        ideal_moves = [ideal_move(grid, x, y) for x, y in a_pos[a]]
        ideal_moves = [m for m in ideal_moves if m]
        ideal_moves = sorted(ideal_moves, key=lambda p: len(list(shortest_path(grid, *p))), reverse=True)
        if ideal_moves:
            return ideal_moves[0]
    return None


hallway_positions = [
    (1, 1),
    (2, 1),
    (4, 1),
    (6, 1),
    (8, 1),
    (10, 1),
    (11, 1),
]


def move_direction(move):
    (from_x, from_y), (to_x, to_y) = move
    if to_x < from_x:
        return "left"
    return "right"


def move_out_of_the_way(grid, blocked_move, x, y):
    (from_x, from_y), (to_x, to_y) = blocked_move
    valid_pos = [(x, y) for x, y in hallway_positions if x < to_x or x > from_x]
    empty_pos = [(x, y) for x, y in valid_pos if grid[y][x] == '.']
    preferred_pos = sorted(empty_pos, key=lambda p: abs(p[0] - x))
    return (x, y), preferred_pos[0]


def print_state(grid, pending_move, blocking_pos, debug=True):
    if not debug:
        return
    (from_x, from_y), (to_x, to_y) = pending_move
    bx, by = blocking_pos
    print(f"pending move {grid[from_y][from_x]}: {pending_move[0]} -> {pending_move[1]}, blocked_by {grid[by][bx]}: {blocking_pos}")


def go(grid, debug=True):
    print("starting grid")
    print_grid(grid)
    pending_moves = []
    while not is_done(grid):
        if not pending_moves:
            m = next_best_move(grid)
            pending_moves.append(m)
        m = pending_moves.pop()
        b_pos = next_blocking_pos(grid, *m)
        if b_pos:
            print_state(grid, m, b_pos, debug)
            pending_moves.append(m)
            pending_moves.append(move_out_of_the_way(grid, m, *b_pos))
        else:
            do_move(grid, pending_moves, *m)
            print_grid(grid)

    return 1


def run_tests():
    print("running tests")
    assert not is_done(parse(test_input_1))
    assert is_done(parse(done_example))
    print("tests complete")


run_tests()
print("test part 1", go(parse(test_input_1)))
