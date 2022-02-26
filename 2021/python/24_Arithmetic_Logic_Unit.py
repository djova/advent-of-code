#!/usr/bin/env python3
from collections import defaultdict
from os.path import join, dirname, realpath

import math

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '24.txt')
raw_input = open(input_file, 'r').read()


def parse(raw):
    return [l.strip().split() for l in raw.split("\n") if l.strip()]


valid_vars = set(list("wxyz"))


def vars_to_s(vars):
    return " ".join(f"{v}={vars[v]}" for v in "wxyz")


def do_op(op, a, b):
    if op == 'add':
        return a + b
    elif op == 'mul':
        return a * b
    elif op == 'div':
        return math.floor(a / b)
    elif op == 'mod':
        if a < 0 or b <= 0:
            raise Exception("invalid")
        return a % b
    elif op == 'eql':
        return 1 if a == b else 0
    else:
        raise Exception("invalid op")


def grouped_instructions(instructions):
    groups = defaultdict(list)
    i = -1
    for instr in instructions:
        if instr == ['inp', 'w']:
            i += 1
        groups[i].append(instr)
    return groups


class ALU:
    def __init__(self, instructions):
        self.instructions = instructions
        self.grouped = grouped_instructions(instructions)

    def run(self, m_number, chunk_i=None, z_in=None):
        vars = {v: 0 for v in valid_vars}
        if z_in is not None:
            vars['z'] = z_in
        m_i = 0
        instructions = self.grouped[chunk_i] if chunk_i is not None else self.instructions
        for instr in instructions:
            op, a = instr[0], instr[1]
            if op == 'inp':
                n = int(m_number[m_i])
                m_i += 1
                if n == 0:
                    raise Exception("invalid")
                vars[a] = n
                continue

            b = instr[2]
            b_val = vars[b] if b in valid_vars else int(b)
            a_val = vars[a]
            new_a_val = do_op(op, a_val, b_val)
            vars[a] = new_a_val

        if m_i < len(m_number) - 1:
            raise Exception("didn't consume entire input number")

        return vars['z']


def run_alu(instructions, m_number):
    return ALU(instructions).run(m_number)


def run_tests():
    test_1 = """\
    inp x
    mul x -1    
    """
    vars = run_alu(parse(test_1), "7")
    assert vars['x'] == -7

    test_2 = """\
    inp z
    inp x
    mul z 3
    eql z x    
    """

    vars = run_alu(parse(test_2), "26")
    assert vars['z'] == 1

    vars = run_alu(parse(test_2), "25")
    assert vars['z'] == 0

    test_3 = """\
    inp w
    add z w
    mod z 2
    div w 2
    add y w
    mod y 2
    div w 2
    add x w
    mod x 2
    div w 2
    mod w 2    
    """

    vars = run_alu(parse(test_3), "3")
    bnum = ''.join([str(vars[c]) for c in "wxyz"])
    assert bnum == "0011"

    run_alu(parse(raw_input), "13579246899999")

    try:
        run_alu(parse(raw_input), "1357924689999999999")
    except Exception as e:
        assert "didn't consume" in str(e)


def search(alu, chunk_i, z_out):
    if chunk_i < 0:
        return ""
    valid_zin = [0] if chunk_i == 0 else range(30)
    for z_in in valid_zin:
        for m_in in range(1, 10):
            m_in = str(m_in)
            z = alu.run(m_in, chunk_i=chunk_i, z_in=z_in)
            if z != z_out:
                continue
            for remainder_m_in in search(alu, chunk_i - 1, z_in):
                yield m_in + remainder_m_in


def part1(instructions):
    print("running part1")
    alu = ALU(instructions)
    max_i = max([int(i) for i in search(alu, 13, 0)])
    print("result", max_i)


part1(parse(raw_input))

"""
understand this one 
https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hpv7g7j/?utm_source=share&utm_medium=web2x&context=3 

from utils import open_day

digits = dict()
stack = list()

with open_day(24) as f:
    dig = 0
    for i, line in enumerate(f):
        _, *operands = line.rstrip().split(' ')
        if i % 18 == 4: push = operands[1] == '1'
        if i % 18 == 5: sub = int(operands[1])
        if i % 18 == 15:
            if push:
                stack.append((dig, int(operands[1])))
            else:
                sibling, add = stack.pop()
                diff = add + sub
                if diff < 0:
                    digits[sibling] = (-diff + 1, 9)
                    digits[dig] = (1, 9 + diff)
                else:
                    digits[sibling] = (1, 9 - diff)
                    digits[dig] = (1 + diff, 9)
            dig += 1

print(''.join(str(digits[d][1]) for d in sorted(digits.keys())))
print(''.join(str(digits[d][0]) for d in sorted(digits.keys())))
"""
