#!/usr/bin/env python3
import itertools
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '07.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().split(',')]


def run_phases(phases, memory, feedback=False):
    ics = [Intcode(memory, [p]) for p in phases]
    signals = [0]
    while True:
        for ic in ics:
            ic.inputs = signals + ic.inputs
            next_signals = list(ic.run_safe())
            if not next_signals:
                return signals[0]
            else:
                signals = next_signals
        if not feedback:
            return signals[0]


def run_tests():
    max_signal = run_phases([4, 3, 2, 1, 0], [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0])
    print("test1-pass:", max_signal == 43210)

    max_signal = run_phases([0, 1, 2, 3, 4],
                            [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24,
                             23, 23, 4, 23, 99, 0, 0])
    print("test2-pass:", max_signal == 54321)

    max_signal = run_phases([1, 0, 4, 3, 2],
                            [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1,
                             33,
                             31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0])
    print("test3-pass:", max_signal == 65210)

    max_signal = run_phases([9, 8, 7, 6, 5], [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                                              27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5], feedback=True)
    print("test4-pass:", max_signal == 139629729)

    max_signal = run_phases([9, 7, 8, 5, 6],
                            [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26,
                             1001, 54,
                             -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55,
                             53, 4,
                             53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10], feedback=True)
    print("test5-pass:", max_signal == 18216)


run_tests()


def part1():
    return max(run_phases(p, input_ints) for p in itertools.permutations([0, 1, 2, 3, 4]))


print(part1())


def part2():
    return max(run_phases(p, input_ints, feedback=True) for p in itertools.permutations([9, 7, 8, 5, 6]))


print(part2())
