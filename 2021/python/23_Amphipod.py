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

rooms = desired_a.keys()

invalid_hallway_points = {
    (3, 1),
    (5, 1),
    (7, 1),
    (9, 1),
}

hallway_endpoints = (
    (1, 1),
    (11, 1)
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
    dx, dy = abs(x - to_x), abs(y - to_y)
    if y > 1 and to_y > 1:
        return dx + abs(1 - to_y) + abs(1 - y)
    return dx + dy


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

    def move(self, from_pos, to_pos, debug=False):
        nb = self.copy()
        (from_x, from_y), (to_x, to_y) = from_pos, to_pos
        a = nb.grid[from_y][from_x]
        nb.grid[to_y][to_x] = a
        nb.grid[from_y][from_x] = '.'
        m_cost = distance(from_pos, to_pos) * a_costs[a]
        nb.moves = nb.moves + ((from_pos, to_pos, m_cost),)
        nb.total_cost += m_cost
        if debug:
            print(f"move {a}: {from_pos} -> {to_pos}, cost={m_cost}")
        return nb

    def a_positions(self):
        positions = defaultdict(list)
        for x, y in itergrid(self.grid):
            c = self.grid[y][x]
            if c in a_costs:
                positions[c].append((x, y))
        return positions

    def room_assignments(self):
        a_positions = self.a_positions()
        result = []
        for a, room_x in desired_room_x.items():
            a_pos = a_positions[a]
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

    def estimated_cost(self):
        cost = 0
        for a, from_pos, to_pos in self.room_assignments():
            if from_pos == to_pos:
                continue
            cost += a_costs[a] * distance(from_pos, to_pos)
        return cost

    def is_done(self):
        invalid, valid = self.room_states()
        if invalid or list(self.hallway_members()):
            return False
        return True

    def total_heuristic_cost(self):
        return self.total_cost

    def __lt__(self, other):
        return self.total_heuristic_cost() < other.total_heuristic_cost()

    def print(self):
        print("\n".join([''.join(row) for row in self.grid]) + "\n")

    def clear_path(self, from_pos, to_pos):
        for (next_x, next_y), steps in shortest_path(from_pos, to_pos):
            if self.grid[next_y][next_x] != '.':
                return False
        return True

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

    def iter_room(self, room_x):
        max_y = 1 + self.room_depth
        for i in range(self.room_depth):
            y = max_y - i
            c = self.grid[y][room_x]
            yield c, (room_x, y)

    def room_has_invalid_members(self, room_x):
        a = desired_a[room_x]
        for c, _ in self.iter_room(room_x):
            if c == '.':
                continue
            if c != a:
                return True
        return False

    def room_states(self):
        invalid, valid = set(), set()
        for room_x in rooms:
            if self.room_has_invalid_members(room_x):
                invalid.add(room_x)
            else:
                valid.add(room_x)
        return invalid, valid

    def first_member(self, room_x):
        for c, (x, y) in reversed(list(self.iter_room(room_x))):
            if c == '.':
                continue
            return c, (x, y)

    def deepest_valid_room_pos(self, room_x):
        for c, (x, y) in self.iter_room(room_x):
            if c == '.':
                return x, y
        return None

    def hallway_members(self):
        (start_x, y), (end_x, _) = hallway_endpoints
        for x in range(start_x, end_x + 1):
            ga = self.grid[y][x]
            if ga != '.':
                yield ga, (x, y)

    def possible_moves(self):
        invalid, valid = self.room_states()

        # members leaving rooms
        for room_x in invalid:
            a, from_pos = self.first_member(room_x)

            room_x = desired_room_x[a]
            if room_x in valid:
                to_pos = self.deepest_valid_room_pos(desired_room_x[a])
                if to_pos and self.clear_path(from_pos, to_pos):
                    yield from_pos, to_pos
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
                    yield from_pos, next_pos

        for a, from_pos in self.hallway_members():
            room_x = desired_room_x[a]
            if room_x not in valid:
                continue
            to_pos = self.deepest_valid_room_pos(room_x)
            if not to_pos:
                raise Exception("wha")
            if not self.clear_path(from_pos, to_pos):
                continue
            yield from_pos, to_pos


def find_path(o_board, debug=False):
    print("starting grid")
    o_board.print()
    states = []
    heapq.heappush(states, o_board.copy())
    i = 0
    while states:
        board = heapq.heappop(states)
        if board.is_done():
            return board

        for from_pos, to_pos in board.possible_moves():
            n_board = board.move(from_pos, to_pos)
            heapq.heappush(states, n_board)

        i += 1
        if i % 10000 == 0:
            if debug:
                replay_board(o_board, board)
            print(f"i={i} len(states)={len(states)} h_cost={board.total_heuristic_cost()} e_cost={board.estimated_cost()} t_cost={board.total_cost} len(moves)={len(board.moves)}")
            board.print()

        if not states:
            raise Exception("wha")

    raise Exception("failed")


def replay_board(o_board, board):
    print("=============== replay ================")
    o_board.print()
    for from_pos, to_pos, m_cost in board.moves:
        o_board = o_board.move(from_pos, to_pos, debug=True)
        o_board.print()
    print("=============== ending stats ================")
    print(f"finished with e_cost={o_board.estimated_cost()} t_cost={o_board.total_cost} sanity_cost={sum(c for _, _, c in o_board.moves)}")


def go(board, debug=False):
    end_board = find_path(board, debug)
    replay_board(board, end_board)
    return end_board.total_cost


test_state_problem = """\
#############
#AA.......BC#
###.#B#D#.###
###.#C#B#.###
###D#B#A#D###
###C#C#A#D###
#############
"""

test_filter_completed = """\
#############
#.......D...#
###.#B#C#D###
###A#B#C#A###
#############
"""


def run_tests():
    print("running tests")
    assert not Board(parse(test_input_1)).is_done()
    assert Board(parse(done_example)).is_done()

    print(f"test distance")
    assert distance((9, 2), (10, 1)) == 2
    assert distance((9, 2), (7, 2)) == 4
    assert distance((9, 2), (7, 3)) == 5
    assert distance((9, 1), (9, 3)) == 2

    print(f"room assignments")
    b = Board(parse(test_input_1))
    b.print()
    for a, from_pos, to_pos in b.room_assignments():
        print(f"ideal {a}: {from_pos} -> {to_pos}")

    print(f"testing problematic state")
    b = Board(parse(test_state_problem))
    b.print()
    for from_pos, to_pos in b.possible_moves():
        x, y = from_pos
        a = b.grid[y][x]
        print(f"move {a}: {from_pos} -> {to_pos}")

    print(f"test filter completed")
    b = Board(parse(test_filter_completed))
    b.print()
    for from_pos, to_pos in b.possible_moves():
        nb = b.move(from_pos, to_pos, debug=True)
        nb.print()

    print("tests complete")


# run_tests()
print("test part 1 (expected 12521)", go(Board(parse(test_input_1)), debug=False))
# print("part 1 (answer 14460)", go(Board(parse(part_1_input))))

# print("test part 2 (expected 44169)", go(Board(parse(test_input_2))))

# correct: 14460
# print("part 1", go(Board(parse(part_1_input))))
# print("part 2", go(Board(parse(part_2_input))))
