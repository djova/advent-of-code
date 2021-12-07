#!/usr/bin/env python3
from collections import Counter, defaultdict
from os.path import join, dirname, realpath

import re

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '06.txt')
raw_input = open(input_file, 'r').read()

# reproduction rate: double every 7 days
# 2 days for 1st cycle of new fish

test_input1 = """\
3,4,3,1,2
"""


def parse(raw):
    return [int(x) for x in re.findall(r"\d+", raw)]


def simulate(fish, days):
    counts = Counter(fish)
    for i in range(days):
        new_counts = defaultdict(int)
        for timer, count in counts.items():
            if timer == 0:
                new_counts[6] += count
                new_counts[8] += count
            else:
                new_counts[timer - 1] += count
        counts = new_counts
    return f"total fish after {days} days: {sum(counts.values())}"


print("Part 1 (test): ", simulate(parse(test_input1), 18))
print("Part 1 (test): ", simulate(parse(test_input1), 80))
print("Part 1 (test): ", simulate(parse(test_input1), 256))

# too low: 25304
print("Part 1: ", simulate(parse(raw_input), 80))
print("Part 1: ", simulate(parse(raw_input), 256))
