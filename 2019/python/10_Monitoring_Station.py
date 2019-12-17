#!/usr/bin/env python3
import math
from collections import defaultdict
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '10.txt')
input_map = open(input_file, 'r').read()

test1 = """\
.#..#
.....
#####
....#
...##
"""

test2 = """\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

test3 = """\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

test4 = """\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

test5 = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""


def iter_asteroids(grid):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == '#':
                yield x, y


def get_angle(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    deg = math.atan2(dy, dx) * 180 / math.pi
    d = (deg + 90) % 360
    return d


def distance(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def asteroids_by_angle(asteroids, origin):
    a_by_angle = defaultdict(list)
    for a in asteroids:
        a_by_angle[get_angle(origin, a)].append(a)
    return a_by_angle


def num_detectable(asteroids, point):
    candidates = asteroids - set([point])
    a_by_angle = asteroids_by_angle(candidates, point)
    return len(a_by_angle)


def find_best_location(map):
    grid = map.split('\n')
    asteroids = set(iter_asteroids(grid))
    detectable = [(a, num_detectable(asteroids, a)) for a in asteroids]
    return max(detectable, key=lambda d: d[1])


def run_laser(map, origin):
    grid = map.split('\n')
    asteroids = set(iter_asteroids(grid)) - set([origin])
    a_by_angle = asteroids_by_angle(asteroids, origin)
    a_by_angle = {a: sorted(l, key=lambda p: distance(p, origin)) for a, l in a_by_angle.items()}
    sorted_angles = sorted(a_by_angle.keys())
    while asteroids:
        for angle in sorted_angles:
            inline = a_by_angle[angle]
            if inline:
                vaporized = inline.pop(0)
                yield vaporized
                asteroids.remove(vaporized)


def run_tests():
    assert get_angle((0, 0), (0, -1)) == 0
    assert get_angle((0, 0), (1, 0)) == 90
    assert get_angle((0, 0), (0, 1)) == 180
    assert get_angle((0, 0), (-1, 0)) == 270

    print("running test1")
    assert find_best_location(test1) == ((3, 4), 8)
    print("running test2")
    assert find_best_location(test2) == ((5, 8), 33)
    print("running test3")
    assert find_best_location(test3) == ((1, 2), 35)
    print("running test4")
    assert find_best_location(test4) == ((6, 3), 41)
    print("running test5")
    assert find_best_location(test5) == ((11, 13), 210)

    v = list(run_laser(test5, (11, 13)))
    assert v[0] == (11, 12)
    assert v[1] == (12, 1)
    assert v[2] == (12, 2)
    assert v[9] == (12, 8)
    assert v[19] == (16, 0)
    assert v[49] == (16, 9)
    assert v[199] == (8, 2)


run_tests()

print("part1")
print(find_best_location(input_map))

print('part2')
x = list(run_laser(input_map, (27, 19)))[199]
print(x[0] * 100 + x[1])
