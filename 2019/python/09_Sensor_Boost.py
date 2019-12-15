#!/usr/bin/env python3
import itertools
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '09.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().split(',')]


def run_tests():
    test1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert list(Intcode(test1).run()) == test1


run_tests()
