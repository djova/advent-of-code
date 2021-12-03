#!/usr/bin/env python3
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '15.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().split(',')]

NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4

WALL = 0
STEP = 1
OXYGEN = 2

VALID_OUTPUT = {WALL, STEP, OXYGEN}

VECTORS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0)
}

INVERSE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST,
}


class Robot:
    def __init__(self):
        self.ic = Intcode(input_ints)
        self.grid = {}
        self.pos = (0, 0)
        self.moves = []

    def next_pos(self, move):
        dx, dy = VECTORS[move]
        return self.pos[0] + dx, + self.pos[1] + dy

    def move(self, move):
        next_pos = self.next_pos(move)
        self.ic.add_input(move)
        output = list(self.ic.run_safe())[0]
        if output not in VALID_OUTPUT:
            raise Exception(f"invalid output {output}")
        self.grid[next_pos] = output
        if output == WALL:
            return None
        self.pos = next_pos
        return self.pos

    def new_move(self):
        for move in [NORTH, SOUTH, EAST, WEST]:
            next_pos = self.next_pos(move)
            if next_pos in self.grid:
                continue
            pos = self.move(move)
            if pos:
                return move
        return None

    def map_grid(self):
        move = self.new_move()
        if not move:
            raise Exception("first move failed")
        self.moves.append(move)
        while self.moves:
            move = self.new_move()
            if move:
                self.moves.append(move)
            else:
                self.move(INVERSE[self.moves.pop()])


def shortest_path(grid, start, end):
    
    return []


def solve_maze():
    r = Robot()
    r.map_grid()
    grid = r.grid
    start, end = (0, 0), [(x, y) for x, y in grid.keys() if grid[(x, y)] == 2][0]
    path = shortest_path(grid, start, end)
    print(f"shortest path {len(path)}")


solve_maze()
