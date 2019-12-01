#!/usr/bin/env python

from os.path import join, realpath, dirname
from collections import Counter

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '01.txt')


def read_ints():
    with open(input_file, 'r') as f:
        return [int(l.strip()) for l in f.readlines()]


def part_1():
    print sum(read_ints())


def part_2(max_loops=1000):
    ints = read_ints()
    counter = Counter()
    current_frequency = 0
    for _ in range(max_loops):
        for i in ints:
            current_frequency += i
            counter.update([current_frequency])
            if counter[current_frequency] > 1:
                print "count({}): {}".format(current_frequency, counter[current_frequency])
                return
    raise Exception('no solution in max loops: {}'.format(max_loops))


part_1()
part_2()
