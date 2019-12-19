#!/usr/bin/env python3
import copy
import itertools
import math
import re
from functools import reduce

from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '12.txt')
raw_input = open(input_file, 'r').read()

test1 = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""


def parse_moons(raw):
    for s in raw.split('\n'):
        match = re.match('<x=(.*), y=(.*), z=(.*)>', s.strip())
        if match:
            yield list(int(i) for i in match.groups())


def apply_gravity(a, b):
    if a == b:
        return 0
    elif a > b:
        return 1
    else:
        return -1


def run_single_dim_step(pos, vel):
    planets = range(len(pos))
    for a, b in itertools.combinations(planets, 2):
        dv = apply_gravity(pos[b], pos[a])
        vel[a] = vel[a] + dv
        vel[b] = vel[b] - dv
    for p in planets:
        pos[p] = pos[p] + vel[p]
    return pos, vel


def run_simulation(raw_moons):
    moons = list(parse_moons(raw_moons))
    pos = [list(z) for z in zip(*moons)]
    vel = [[0 for _ in range(len(moons))] for _ in range(len(pos))]
    while True:
        for d in range(len(pos)):
            pos[d], vel[d] = run_single_dim_step(pos[d], vel[d])
        yield pos, vel


def end_energy(raw_moons, steps):
    pos, vel = list(itertools.islice(run_simulation(raw_moons), steps))[-1]
    potential = [sum(abs(i) for i in mp) for mp in zip(*pos)]
    kinetic = [sum(abs(i) for i in mp) for mp in zip(*vel)]
    return sum(a * b for a, b in zip(potential, kinetic))


def lcm(a, b):
    a, b = int(a), int(b)
    return int(abs(a * b) / math.gcd(a, b))


def run_until_duplicate_pos(raw_moons):
    moons = list(parse_moons(raw_moons))
    pos = [list(z) for z in zip(*moons)]
    vel = [[0 for _ in range(len(moons))] for _ in range(len(pos))]
    dim_repeat_steps = []
    for initial_state in zip(pos, vel):
        step = 0
        state = [copy.copy(l) for l in initial_state]
        while True:
            step += 1
            state = run_single_dim_step(*state)
            if state == initial_state:
                dim_repeat_steps.append(step)
                break
    return reduce(lcm, dim_repeat_steps)


print("test1 total-energy", end_energy(test1, 10))
print("part1 total-energy", end_energy(raw_input, 1000))
print("test1 duplicate-pos", run_until_duplicate_pos(test1))
print("part1 duplicate-pos", run_until_duplicate_pos(raw_input))
