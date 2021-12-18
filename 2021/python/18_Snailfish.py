#!/usr/bin/env python3
from os.path import join, dirname, realpath

import math

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '18.txt')
raw_input = open(input_file, 'r').read()

test_input = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


def parse(raw):
    return [[int(c) if c.isdigit() else c for c in s.strip()] for s in raw.split("\n") if s.strip()]


def add(a, b):
    return ["["] + a + [","] + b + ["]"]


def find_exploding_pair(line):
    depth = 0
    last_open_i = 0
    for i, c in enumerate(line):
        if c == '[':
            depth += 1
            last_open_i = i
            continue
        elif c == ']':
            depth -= 1
            if depth == 4 and i - last_open_i == 4:
                return last_open_i
            continue
    return None


def find_split(line):
    for i, c in enumerate(line):
        if isinstance(c, int):
            if c >= 10:
                return i
    return None


def fmtline(line):
    return "".join([str(c) for c in line])


def reduce(line, debug=False):
    while True:
        if debug:
            print(f"reducing: {fmtline(line)}")
        if pi := find_exploding_pair(line):
            if debug:
                print(f"exploding i={pi}: {fmtline(line[pi:pi + 5])}", )
            ai, bi = pi + 1, pi + 3
            a, b = line[ai], line[bi]
            ai, bi = ai - 1, bi + 1
            while ai >= 0:
                if isinstance(line[ai], int):
                    line[ai] += a
                    break
                ai -= 1
            while bi < len(line):
                if isinstance(line[bi], int):
                    line[bi] += b
                    break
                bi += 1
            line = line[0:pi] + [0] + line[pi + 5:]
            continue
        if si := find_split(line):
            if debug:
                print(f"splitting i={si}: {line[si]}")
            n = line[si]
            line = line[0:si] + ['[', math.floor(n / 2), ',', math.ceil(n / 2), ']'] + line[si + 1:]
            continue
        return line


def magnitude(line):
    pending = []
    for c in line:
        if isinstance(c, int):
            pending.append(c)
            continue
        if c == ']':
            b = pending.pop()
            pending[-1] = 3 * pending[-1] + 2 * b
            continue
    return pending[0]


def go(lines, debug=False):
    if not lines:
        return lines
    agg = lines[0]
    for line in lines[1:]:
        agg = reduce(add(agg, line), debug=debug)
    if debug:
        print(f"final sum: {fmtline(agg)}")
    return magnitude(agg)


print("test magnitude. expected=143: ", magnitude(parse("[[1,2],[[3,4],5]]")[0]))
print("test magnitude. expected=1384: ", magnitude(parse("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")[0]))
print("test magnitude. expected=445: ", magnitude(parse("[[[[1,1],[2,2]],[3,3]],[4,4]]")[0]))
print("test magnitude. expected=791: ", magnitude(parse("[[[[3,0],[5,3]],[4,4]],[5,5]]")[0]))
print("test magnitude. expected=1137: ", magnitude(parse("[[[[5,0],[7,4]],[5,5]],[6,6]]")[0]))
print("test magnitude. expected=3488: ", magnitude(parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")[0]))
print("test: ", go(parse(test_input), debug=True))
print("part 1: ", go(parse(raw_input)))
