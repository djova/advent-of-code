#!/usr/bin/env python3
from collections import defaultdict
from functools import cached_property

import heapq

test_input_1 = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

test_input_2 = """\
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
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

part_1_input = """\
#############
#...........#
###D#B#D#A###
  #C#C#A#B#
  #########
"""

part_2_input = """\
#############
#...........#
###D#B#D#A###
  #D#C#B#A#
  #D#B#A#C#
  #C#C#A#B#
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

desired_room_x = {
    'A': 3,
    'B': 5,
    'C': 7,
    'D': 9,
}

desired_a = {v: k for k, v in desired_room_x.items()}

invalid_hallway_points = {
    (3, 1),
    (5, 1),
    (7, 1),
    (9, 1),
}

hallway_endpoints = (
    (1, 1),
    (12, 1)
)


def itergrid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            yield x, y


def shortest_path(from_p, to_p):
    (x, y), (to_x, to_y) = from_p, to_p
    steps = 0
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
        steps += 1
        yield (x, y), steps


def distance(from_p, to_p):
    (x, y), (to_x, to_y) = from_p, to_p
    if x == to_x:
        return abs(y - to_y)
    return abs(to_x - x) + abs(y - to_y) + abs(1 - y)


class Board:
    def __init__(self, grid):
        self.grid = [r[:] for r in grid]
        self.room_depth = len(self.grid) - 3
        self.total_cost = 0
        self.moves = ()

    def copy(self):
        nb = Board(self.grid)
        nb.total_cost = self.total_cost
        nb.moves = self.moves
        return nb

    def move(self, move_from, move_to, m_cost):
        nb = self.copy()
        (from_x, from_y), (to_x, to_y) = move_from, move_to
        nb.grid[to_y][to_x] = nb.grid[from_y][from_x]
        nb.grid[from_y][from_x] = '.'
        nb.moves = nb.moves + ((move_from, move_to, m_cost),)
        nb.total_cost += m_cost
        return nb

    @cached_property
    def a_positions(self):
        positions = defaultdict(list)
        for x, y in itergrid(self.grid):
            c = self.grid[y][x]
            if c in a_costs:
                positions[c].append((x, y))
        return positions

    @cached_property
    def room_assignments(self):
        result = []
        for a, room_x in desired_room_x.items():
            a_pos = self.a_positions[a]
            room_y = 1 + self.room_depth
            end_room = (room_x, room_y)
            a_pos = sorted(a_pos, key=lambda p: distance(p, end_room))
            for from_pos, i in zip(a_pos, range(self.room_depth)):
                to_pos = (room_x, room_y - i)
                result.append((a, from_pos, to_pos))
        return result

    def next_valid_room_pos(self, x):
        y = 1 + self.room_depth
        for i in range(self.room_depth):
            a = self.grid[y - i][x]
            if a == '.':
                return (x, y)
            if a != desired_a[x]:
                return None
        return None

    @cached_property
    def estimated_cost(self):
        cost = 0
        for a, from_pos, to_pos in self.room_assignments:
            if from_pos == to_pos:
                continue
            from_x, from_y = from_pos
            a = self.grid[from_y][from_x]
            cost += distance(from_pos, to_pos) * a_costs[a]
        return cost

    @cached_property
    def total_heuristic_cost(self):
        return self.estimated_cost + self.total_cost

    def __lt__(self, other):
        return self.total_heuristic_cost < other.total_heuristic_cost

    def print(self):
        print("\n" + "\n".join([''.join(row) for row in self.grid]) + "\n")

    def clear_path(self, from_pos, to_pos):
        last_pos, last_steps = None, None
        for (next_x, next_y), steps in shortest_path(from_pos, to_pos):
            if self.grid[next_y][next_x] != '.':
                return None, None
            last_pos, last_steps = (next_x, next_y), steps
        return last_pos, last_steps

    def best_valid_room_pos(self, to_pos):
        x, _ = to_pos
        max_y = 1 + self.room_depth
        for i in range(self.room_depth):
            y = max_y - i
            a = self.grid[y][x]
            if a == '.':
                return x, y
            if a != desired_a[x]:
                return None
        return None

    def possible_moves(self):
        for a, from_pos, to_pos in self.room_assignments:
            if from_pos == to_pos:
                continue

            to_pos = self.best_valid_room_pos(to_pos)
            if to_pos:
                to_pos, steps = self.clear_path(from_pos, to_pos)
                if to_pos:
                    yield from_pos, to_pos, steps * a_costs[a]
                    continue

            if from_pos[1] == 1:
                # hallway
                continue

            for d in hallway_endpoints:
                for next_pos, steps in shortest_path(from_pos, d):
                    next_x, next_y = next_pos
                    if self.grid[next_y][next_x] != '.':
                        break
                    if next_pos in invalid_hallway_points:
                        continue
                    if next_y > 1:
                        continue
                    yield from_pos, next_pos, steps * a_costs[a]


def find_path(o_board, debug=False):
    print("starting grid")
    o_board.print()
    states = []
    heapq.heappush(states, o_board.copy())
    i = 0
    while states:
        board = heapq.heappop(states)
        if board.estimated_cost == 0:
            return board

        for from_pos, to_pos, m_cost in board.possible_moves():
            n_board = board.move(from_pos, to_pos, m_cost)
            heapq.heappush(states, n_board)

        i += 1
        if i % 10000 == 0:
            if debug:
                replay_board(o_board, board)
            print(f"i={i} len(states)={len(states)} h_cost={board.total_heuristic_cost} e_cost={board.estimated_cost} t_cost={board.total_cost} len(moves)={len(board.moves)}")
            board.print()


def replay_board(o_board, board):
    print("=============== replay ================")
    o_board.print()
    for from_pos, to_pos, m_cost in board.moves:
        x, y = from_pos
        print(f"move {o_board.grid[y][x]}: {from_pos} -> {to_pos} cost={m_cost}")
        o_board = o_board.move(from_pos, to_pos, m_cost)
        o_board.print()
    print("=============== ending stats ================")
    print(f"finished with e_cost={o_board.estimated_cost} t_cost={o_board.total_cost} sanity_cost={sum(c for _, _, c in o_board.moves)}")


def go(board):
    end_board = find_path(board)
    replay_board(board, end_board)


test_state_problem = """\
#############
#AA.......BC#
###.#B#D#.###
###.#C#B#.###
###D#B#A#D###
###C#C#A#D###
#############
"""


def run_tests():
    print("running tests")
    assert Board(parse(test_input_1)).estimated_cost > 0
    assert Board(parse(done_example)).estimated_cost == 0
    print(f"room assignments")
    b = Board(parse(test_input_1))
    b.print()
    for a, from_pos, to_pos in b.room_assignments:
        print(f"ideal {a}: {from_pos} -> {to_pos}")

    print(f"testing problematic state")
    b = Board(parse(test_state_problem))
    b.print()
    for from_pos, to_pos, cost in b.possible_moves():
        x, y = from_pos
        a = b.grid[y][x]
        print(f"move {a}: {from_pos} -> {to_pos}")

    print("tests complete")


# run_tests()
# print("test part 1", go(Board(parse(test_input_1))))
print("test part 2", go(Board(parse(test_input_2))))

# correct: 14460
# print("part 1", go(Board(parse(part_1_input))))
# print("part 2", go(Board(parse(part_2_input))))
