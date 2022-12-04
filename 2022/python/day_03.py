#!/usr/bin/env python3
import re
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()

test_input_text = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

letters = "abcdefghijklmnopqrstuvwxyz"
letter_scores = {}

for i, c in enumerate(letters):
    i += 1
    letter_scores[c] = i

for i, c in enumerate(letters.upper()):
    i += 27
    letter_scores[c] = i


def part1(raw_input):
    result = 0
    lines = [s.strip() for s in raw_input.split('\n') if s.strip()]
    for line in lines:
        mid = int(len(line) / 2)
        a, b = line[0:mid], line[mid:]
        common = set(a).intersection(set(b))
        bag_score = sum(letter_scores[c] for c in common)
        result += bag_score
    return result


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def part2(raw_input):
    result = 0
    lines = [s.strip() for s in raw_input.split('\n') if s.strip()]
    for group in chunks(lines, 3):
        group_sets = [set(g) for g in group]
        f = group_sets[0]
        for g in group_sets[1:]:
            f = f.intersection(g)
        badge_type = list(f)[0]
        result += letter_scores[badge_type]
    return result


def test_part1():
    assert part1(test_input_text) == 157


def test_part2():
    assert part2(test_input_text) == 70


print("Part 1: ", part1(input_text))
print("Part 2: ", part2(input_text))
