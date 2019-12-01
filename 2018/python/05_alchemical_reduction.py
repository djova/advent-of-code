#!/usr/bin/env python
from os.path import join, realpath, dirname
from string import ascii_lowercase

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '05.txt')


def react_polymer(polymer):
    # stack-based solution
    stack = []
    for c in polymer:
        if not stack:
            stack.append(c)
            continue
        if stack[-1] != c and stack[-1].lower() == c.lower():
            stack.pop()
        else:
            stack.append(c)
    return stack


def polymer_reduction(acc, right):
    # functional solution
    if not acc:
        return right
    if acc[-1] != right and acc[-1].lower() == right.lower():
        return acc[:-1]
    else:
        return acc + right


def filter_chars(s, exclude_chars):
    return [c for c in s if c not in exclude_chars]


def main():
    polymer = open(input_file).readline().strip()

    # part 1
    print len(react_polymer(polymer)), len(reduce(polymer_reduction, polymer))

    # part 2
    pairs = [set(p) for p in zip(ascii_lowercase, ascii_lowercase.upper())]
    print min(len(react_polymer(filter_chars(polymer, p))) for p in pairs)


main()
