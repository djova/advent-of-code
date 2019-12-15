#!/usr/bin/env python3
import itertools
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '09.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().split(',')]


def run_tests():
    test1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert list(Intcode(test1).run()) == test1
    test2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    assert len(str(list(Intcode(test2).run())[0])) == 16
    test3 = [104, 1125899906842624, 99]
    assert list(Intcode(test3).run())[0] == 1125899906842624


run_tests()

print(list(Intcode(input_ints, inputs=[1]).run()))

print(list(Intcode(input_ints, inputs=[2]).run()))
