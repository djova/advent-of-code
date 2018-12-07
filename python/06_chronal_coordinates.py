#!/usr/bin/env python
from collections import namedtuple, Counter, defaultdict
from os.path import join, realpath, dirname

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '06.txt')

test_input = """\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""

Point = namedtuple('Point', ['x', 'y'])


def load_input(test=False):
    raw = test_input if test else open(input_file).read()
    return [Point(*[int(s) for s in s.split(',')]) for s in raw.strip().split('\n')]


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def iter_grid(max_x, max_y):
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            yield Point(x, y)


def main(test=False):
    coordinates = set(load_input(test))
    max_x, max_y = max(p.x for p in coordinates), max(p.y for p in coordinates)

    def _is_edge(p):
        return p.x == 0 or p.x == max_x or p.y == 0 or p.y == max_y

    def get_distances(point):
        distances = defaultdict(list)
        for c in coordinates:
            distances[manhattan_distance(point, c)].append(c)
        return distances

    def closest_coordinate(distances):
        closest_points = distances.get(min(distances.keys()))
        if len(closest_points) == 1:
            return closest_points[0]
        return None

    coordinate_distances = [(p, get_distances(p)) for p in iter_grid(max_x, max_y)]

    # part 1
    closest_coordinates = [(p, closest_coordinate(d)) for p, d in coordinate_distances]
    infinite_coordinates = {c for p, c in closest_coordinates if _is_edge(p)}
    _, d = max(Counter([c for _, c in closest_coordinates if c not in infinite_coordinates]).items(),
               key=lambda x: x[1])
    print d

    # part 2
    def in_region(distances, distance_limit):
        return sum(d * len(p) for d, p in distances.items()) < distance_limit

    distance_limit = 32 if test else 10000
    safe_region = [p for p, d in coordinate_distances if in_region(d, distance_limit)]
    print len(safe_region)


main()
# main(True)
