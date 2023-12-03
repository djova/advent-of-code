#!/usr/bin/env python3
from os.path import join, dirname, realpath

import pytest

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '01.txt')
input_text = open(input_file, 'r').read()

letter_digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

prefix_tree = {}


def _insert_into_tree(tree, key, val):
    if not key:
        return
    head, tail = key[0], key[1:]
    if not tail:
        tree[head] = val
        return
    if head not in tree:
        tree[head] = {}
    _insert_into_tree(tree[head], tail, val)


def _lookup_prefix(tree, key):
    if not key:
        return None
    head, tail = key[0], key[1:]
    if not tail:
        return tree.get(head, None)
    subtree = tree.get(head, None)
    if not subtree or not isinstance(subtree, dict):
        return None
    return _lookup_prefix(subtree, tail)


for k in letter_digits:
    _insert_into_tree(prefix_tree, k, letter_digits[k])


def extract_digits(line):
    i, j = 0, 0
    current_tree = prefix_tree
    while j < len(line):
        c = line[j]
        if c.isdigit():
            yield c
            j += 1
            i = j
            current_tree = prefix_tree
            continue
        if c not in current_tree:
            i += 1
            j = i
            current_tree = prefix_tree
            continue
        current_tree = current_tree[c]
        if isinstance(current_tree, str):
            yield current_tree
            current_tree = prefix_tree
            i += 1
            j = i
            continue
        j += 1


def iter_calibration_ints(raw_input):
    for line in raw_input.split('\n'):
        line = line.strip()
        if not line:
            continue
        ints = list(extract_digits(line))
        yield int(ints[0] + ints[-1])


def sum_calibration_values(raw_input):
    return sum(iter_calibration_ints(raw_input))


def test_prefix_tree():
    for k, v in letter_digits.items():
        assert _lookup_prefix(prefix_tree, k) == v


def test_calibration_sum():
    test_input_text = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
    assert sum_calibration_values(test_input_text) == 142


def test_part_2():
    test_input_text = """\
    two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    assert sum_calibration_values(test_input_text) == 281


@pytest.mark.parametrize("line,expected_digits", [
    ("two1nine", "219"),
    ("eightwothree", "823"),
    ("abcone2threexyz", "123"),
    ("xtwone3four", "2134"),
    ("4nineeightseven2", "49872"),
    ("zoneight234", "18234"),
    ("7pqrstsixteen", "76"),
])
def test_extraction(line, expected_digits):
    assert "".join(extract_digits(line)) == expected_digits


def run_main():
    print(sum_calibration_values(input_text))


if __name__ == '__main__':
    run_main()
