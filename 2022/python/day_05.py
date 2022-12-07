#!/usr/bin/env python3
import re
from collections import defaultdict
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()

test_input_text = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def process_raw_input(raw_input):
    columns = defaultdict(list)
    moves = []
    for line in raw_input.split('\n'):
        if not line.strip():
            continue
        if line.startswith('   ') or line.startswith('['):
            for i in range(0, len(line), 4):
                c = line[i + 1].strip()
                if not c:
                    continue
                col = i // 4 + 1
                columns[col].insert(0, c)
        elif line.startswith('move'):
            moves.append([int(d) for d in re.findall(r'\d+', line)])
    return columns, moves


def part1(raw_input):
    columns, moves = process_raw_input(raw_input)
    for count, from_col, to_col in moves:
        for _ in range(count):
            c = columns[from_col].pop()
            columns[to_col].append(c)
    result = "".join([columns[i][-1] for i in range(1, len(columns.keys()) + 1)])
    return result


def part2(raw_input):
    columns, moves = process_raw_input(raw_input)
    for count, from_col, to_col in moves:
        stack = columns[from_col]
        stack, c = stack[0:-count], stack[-count:]
        columns[to_col].extend(c)
        columns[from_col] = stack
    result = "".join([columns[i][-1] for i in range(1, len(columns.keys()) + 1)])
    return result


def test_part1():
    assert part1(test_input_text) == "CMZ"


def test_part2():
    assert part2(test_input_text) == "MCD"


print("Part 1: ", part1(input_text))
print("Part 2: ", part2(input_text))
