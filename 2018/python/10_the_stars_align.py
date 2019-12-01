#!/usr/bin/env python
import re
import sys
import time
from collections import namedtuple
from os.path import join, realpath, dirname

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '10.txt')

test_input = """\
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""

Coord = namedtuple('Node', ['children', 'metadata'])


def load_input(test):
    raw = test_input if test else open(input_file).read()
    ints = [[int(i) for i in re.findall(r'-?\d+', l)] for l in raw.split('\n') if l]
    return ints


def translate_points(points, time):
    for pos_x, pos_y, vel_x, vel_y in points:
        x = pos_x + time * vel_x
        y = pos_y + time * vel_y
        yield x, y


def print_points(points):
    points = set(points)
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points) + 1
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points) + 1
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (x, y) in points:
                sys.stdout.write('#')
            else:
                sys.stdout.write('.')
        print ""


def main(test=False):
    point_vecs = load_input(test)
    last_width = 0

    for i in range(100000):
        points = {(x, y) for x, y in translate_points(point_vecs, i)}
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points) + 1

        width = max_x - min_x
        if last_width == 0 or width < last_width:
            last_width = width
            continue

        min_time = i - 1
        # part 1
        print_points(translate_points(point_vecs, min_time))
        # part 2
        print "\nTIME: {}".format(min_time)
        time.sleep(1)
        break

    return


main()
