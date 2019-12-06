#!/usr/bin/env python3
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '05.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().split(',')]


def run_tests():
    # opcode, param_modes = parse_instruction(1002)
    # if opcode != 2:
    #     print("wrong opcode")
    # elif param_modes != [0, 1, 0]:
    #     print("wrong param modes")
    # else:
    #     print("tests passed")
    #
    # runcode([3, 0, 4, 0, 99], 444)
    # result = runcode([1002, 4, 3, 4, 33])
    # if result[-1] != 99:
    #     print("failed expected 99")
    #
    po_equal_8 = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]

    Intcode(po_equal_8, 3).run()
    print("expected 0")
    Intcode(po_equal_8, 8).run()
    print("expected 1")
    #
    # po_lt_8 = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    #
    # Intcode(po_lt_8, 9).run()
    # print("expected 0")
    #
    # Intcode(po_lt_8, 3).run()
    # print("expected 1")

    im_equal_8 = [3, 3, 1108, -1, 8, 3, 4, 3, 99]

    Intcode(im_equal_8, 3).run()
    print("expected 0")

    Intcode(im_equal_8, 8).run()
    print("expected 1")

    im_lt_8 = [3, 3, 1107, -1, 8, 3, 4, 3, 99]

    # larger = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
    #           1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
    #           999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    #
    # runcode(larger, 7)
    # print("expected 999")
    # runcode(larger, 8)
    # print("expected 1000")
    # runcode(larger, 9)
    # print("expected 1001")
    return


# run_tests()

Intcode(input_ints, 5).run()
