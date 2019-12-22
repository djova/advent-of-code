#!/usr/bin/env python3
import itertools
import math
import re
import sys
import termios
import time
import tty
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '14.txt')
main_input = open(input_file, 'r').read()

test1 = """\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

test2 = """\
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

test3 = """\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

test4 = """\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""

test5 = """\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""


def parse_reactions(raw):
    reactions = {}
    for r in (r for r in raw.split('\n') if r):
        reaction = [(int(m.group(1)), m.group(2)) for m in re.finditer(r'(\d+) (\w+)', r)]
        inputs, output = reaction[0:-1], reaction[-1]
        if output[1] in reactions:
            raise Exception("two reactions producing the same output")
        reactions[output[1]] = reaction
    return reactions


def ore_needed_for_fuel(raw_reactions, fuel_needed):
    reactions = parse_reactions(raw_reactions)
    needed = {'FUEL': fuel_needed}
    leftover = {}
    ore_needed = 0
    while needed:
        next_chem = list(needed.keys())[0]
        next_count = needed.pop(next_chem)
        reaction = reactions[next_chem]
        inputs, (out_count, _) = reaction[0:-1], reaction[-1]
        multiple = math.ceil(next_count / float(out_count))
        for in_count, in_chem in inputs:
            in_count *= multiple
            if in_chem == 'ORE':
                ore_needed += in_count
            else:
                leftover_used = min(in_count, leftover.get(in_chem, 0))
                leftover[in_chem] = max(0, leftover.get(in_chem, 0) - leftover_used)
                in_count -= leftover_used
                if in_count > 0:
                    needed[in_chem] = needed.get(in_chem, 0) + in_count
        leftover[next_chem] = out_count * multiple - next_count
    #     print("reaction", reaction, "desired", (next_count, next_chem), "multiple", multiple, "produced",
    #           out_count * multiple, "leftover", {k: v for k, v in leftover.items() if v > 0})
    # print("total ore needed", ore_needed)
    return ore_needed


def max_fuel_for_ore(raw_reactions, max_ore):
    fuel_a, fuel_b = 1, 10
    while True:
        ore_needed = ore_needed_for_fuel(raw_reactions, fuel_b)
        if ore_needed > max_ore:
            break
        fuel_a = fuel_b
        fuel_b = fuel_b * 10

    # binary search
    fuel_x = fuel_b
    while fuel_a < fuel_b - 1:
        if ore_needed_for_fuel(raw_reactions, fuel_x) > max_ore:
            fuel_b = fuel_x
        else:
            fuel_a = fuel_x
        fuel_x = fuel_a + math.floor((fuel_b - fuel_a) / 2)

    return fuel_x


def run_tests():
    assert ore_needed_for_fuel(test1, 1) == 31
    assert ore_needed_for_fuel(test2, 1) == 165
    assert ore_needed_for_fuel(test3, 1) == 13312
    assert ore_needed_for_fuel(test4, 1) == 180697
    assert ore_needed_for_fuel(test5, 1) == 2210736
    assert max_fuel_for_ore(test3, 1e12) == 82892753
    assert max_fuel_for_ore(test4, 1e12) == 5586022
    assert max_fuel_for_ore(test5, 1e12) == 460664


run_tests()

print("part1", ore_needed_for_fuel(main_input, 1))
print("part2", max_fuel_for_ore(main_input, 1e12))
