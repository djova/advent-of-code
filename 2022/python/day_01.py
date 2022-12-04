#!/usr/bin/env python3
from os.path import join, dirname, realpath

test_input_text = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '01.txt')
input_text = open(input_file, 'r').read()


def get_elf_totals(inp):
    elves = []
    count = 0
    for l in inp.split('\n'):
        l = l.strip()
        if not l:
            elves.append(count)
            count = 0
            continue
        count += int(l)
    return elves


def sum_top_3(elves):
    return sum(sorted(elves)[-3:])


print("test Part 1: ", max(get_elf_totals(test_input_text)))
print("Part 1: ", max(get_elf_totals(input_text)))

print("test Part 2: ", sum_top_3(get_elf_totals(test_input_text)))
print("Part 2: ", sum_top_3(get_elf_totals(input_text)))
