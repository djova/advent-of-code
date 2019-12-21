#!/usr/bin/env python3
import itertools
import sys
import termios
import time
import tty
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '13.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().split(',')]


def get_ch():
    """Get a single character from stdin, Unix version"""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())  # Raw read
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def draw_tiles(tiles):
    points = tiles.keys()
    max_x = max(p[0] for p in points)
    max_y = max(p[1] for p in points)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(tiles[(x, y)], sep=' ', end='')
        print()
    current_score = tiles.get((-1, 0), None)
    if current_score is not None:
        print("current-score", current_score)


PADDLE = 3
BALL = 4
BLOCK = 2


def run_step(ic, tiles, draw=False):
    it = iter(ic.run_safe())
    while True:
        output = list(itertools.islice(it, 3))
        if not output:
            break
        x, y, tile_id = output
        tiles[(x, y)] = tile_id
        if tile_id == PADDLE:
            tiles[(-1, PADDLE)] = (x, y)
        elif tile_id == BALL:
            tiles[(-1, BALL)] = (x, y)
    if draw:
        draw_tiles(tiles)


LEFT = -1
NEUTRAL = 0
RIGHT = 1


def get_key_input():
    ch = get_ch()
    if ch == 'a':
        return LEFT
    elif ch == 's':
        return NEUTRAL
    elif ch == 'd':
        return RIGHT
    else:
        raise Exception("invalid char " + ch)


def get_auto_input(s1, s2):
    if s1 is None:
        return NEUTRAL
    bdx, bdy = s2[BALL][0] - s1[BALL][0], s2[BALL][1] - s1[BALL][1]
    px, py = s2[PADDLE]
    bx, by = s2[BALL]
    if bdy < 0:
        target_px = bx
    else:
        target_px = (py - by) * bdx + bx
    # time.sleep(0.1)
    if target_px == px:
        return NEUTRAL
    elif target_px < px:
        return LEFT
    else:
        return RIGHT


def get_state(tiles):
    return {
        BALL: tiles[(-1, BALL)],
        PADDLE: tiles[(-1, PADDLE)],
    }


def run(automatic=False):
    input_ints[0] = 2
    ic = Intcode(input_ints)
    tiles = {}
    s1 = None
    run_step(ic, tiles, draw=True)
    s2 = get_state(tiles)
    while True:
        i = get_auto_input(s1, s2) if automatic else get_key_input()
        ic.add_input(i)
        s1 = s2
        run_step(ic, tiles, draw=True)
        s2 = get_state(tiles)
        if s2[BALL][1] > s2[PADDLE][1]:
            print("GAME OVER!")
            break
        if BLOCK not in tiles.values():
            print("WIN!")
            break


def run_test():
    s1 = {BALL: (20, 10), PADDLE: (22, 20)}
    s2 = {BALL: (20, 11), PADDLE: (22, 20)}
    assert get_auto_input(s1, s2) == LEFT


# run_test()
run(True)
