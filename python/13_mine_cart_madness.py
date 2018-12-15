#!/usr/bin/env python
import sys
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '13.txt')

test_input = """\
/->-\        
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""


def transpose(grid):
    t_grid = [[None for _ in range(len(grid))] for _ in range(len(grid[0]))]
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            t_grid[x][y] = cell
    return t_grid


def load_input(test=False):
    raw = test_input if test else open(input_file).read()
    grid = [l for l in raw.split('\n') if l]
    return transpose(grid)


def iter_grid(grid):
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            yield x, y


cart_dir = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}

dir_to_cart = {d: c for c, d in cart_dir.items()}

# assume all carts are initially located on a horizontal or vertical road, never turn or intersection
cart_to_road = {
    '<': '-',
    '>': '-',
    '^': '|',
    'v': '|',
}


def find_carts(grid):
    for x, y in iter_grid(grid):
        if grid[x][y] in cart_dir:
            yield (x, y), cart_dir[grid[x][y]]


def print_grid(grid, carts, crashes):
    for x, y in iter_grid(grid):
        if x == 0:
            print ""

        point = (x, y)
        if point in crashes:
            sys.stdout.write('X')
        elif point in carts:
            vec, _ = carts[point]
            sys.stdout.write(dir_to_cart[vec])
        else:
            sys.stdout.write(grid[x][y])


# left turn
# right (1, 0) -> up (0, -1)
# up (0, -1) -> left (-1, 0)
# left (-1, 0) -> down (0, 1)
# down (0, 1) -> right (1, 0)

def turn_left((x, y)):
    return (y, -x)


def turn_right((x, y)):
    return (-y, x)


def right_slash((x, y)):
    return (-y, -x)


# right slash
# right (1, 0) -> up (0, -1)
# up (0, -1) -> right (1, 0)
# left (-1, 0) -> down (0, 1)
# down (0, 1) -> left (-1, 0)

# left slash
# right (1, 0) -> down (0, 1)
# up (0, -1) -> left (-1, 0)
# left (-1, 0) -> up (0, -1)
# down (0, 1) -> right (1, 0)


def left_slash((x, y)):
    return (y, x)


def straight(vec):
    return vec


turn_rules = [turn_left, straight, turn_right]


def do_turn(vec, turns):
    return turn_rules[turns % len(turn_rules)](vec)


def move_cart(grid, point, vec, turns):
    point = tuple(a + b for a, b in zip(point, vec))
    nx, ny = point
    nc = grid[nx][ny]
    if nc == '+':
        vec = do_turn(vec, turns)
        turns += 1
    elif nc == '/':
        vec = right_slash(vec)
    elif nc == '\\':
        vec = left_slash(vec)
    return point, vec, turns


def run_simulation(grid, debug=False):
    carts = {point: (vec, 0) for point, vec in find_carts(grid)}
    crashed = {}

    # replace carts
    grid = [[cart_to_road.get(c, c) for c in row] for row in grid]

    while True:
        if debug:
            print_grid(grid, carts, crashed)

        for point in sorted(carts.keys()):
            if point not in carts:
                continue
            vec, turns = carts.pop(point)
            n_point, n_vec, n_turns = move_cart(grid, point, vec, turns)
            if n_point in carts:
                crashed[n_point] = True
                carts.pop(n_point)
            else:
                carts[n_point] = (n_vec, n_turns)

        yield carts, crashed


def run_until_first_crash(grid, debug=False):
    for carts, crashed in run_simulation(grid, debug):
        if crashed:
            return crashed.keys()[0]


def run_until_last_cart(grid, debug=False):
    for carts, crashed in run_simulation(grid, debug):
        if len(carts) == 1:
            return carts.keys()[0]


def run_tests():
    crash_point = run_until_first_crash(load_input(True), True)
    expected_point = (7, 3)
    if crash_point == expected_point:
        print "correct crash point: {}".format(crash_point)
    else:
        print "wrong crash point: {} != {}".format(crash_point, expected_point)


def main():
    grid = load_input()

    # part 1
    print run_until_first_crash(grid)

    # part 2
    print run_until_last_cart(grid)


# run_tests()
main()
