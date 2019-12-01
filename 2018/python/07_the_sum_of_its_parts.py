#!/usr/bin/env python
import re
from collections import namedtuple, defaultdict
from itertools import chain
from os.path import join, realpath, dirname
from string import ascii_uppercase

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '07.txt')

test_input = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""

Point = namedtuple('Point', ['x', 'y'])


def load_input(test=False):
    raw = test_input if test else open(input_file).read()

    def _parse(l):
        return re.match("Step (\w) must be finished before step (\w) can begin.\s*", l).groups()

    return [_parse(l) for l in raw.split('\n') if l]


def main(test=False):
    dependencies = load_input(test)

    lookup = defaultdict(list)
    for dependency, step in dependencies:
        lookup[step].append(dependency)

    def _find_leaves(_remaining):
        for step in _remaining:
            live_deps = [d for d in lookup[step] if d in _remaining]
            if not live_deps:
                yield step

    # part 1
    remaining = set(chain(*dependencies))
    sorted_steps = []
    while remaining:
        leaf = sorted(_find_leaves(remaining))[0]
        remaining.remove(leaf)
        sorted_steps.append(leaf)
    print ''.join(sorted_steps)

    # part 2
    time_offset = 1 if test else 61
    time_per_step = dict(zip(ascii_uppercase, range(time_offset, len(ascii_uppercase) + time_offset)))
    remaining = set(chain(*dependencies))
    in_progress = {}
    current_time = 0
    workers = 2 if test else 5

    while remaining:
        finished_steps = [step for step, end_time in in_progress.items() if end_time == current_time]
        for step in finished_steps:
            in_progress.pop(step)
            remaining.remove(step)

        leaves = [l for l in sorted(_find_leaves(remaining)) if l not in in_progress]
        for leaf in leaves[0:workers - len(in_progress)]:
            in_progress[leaf] = current_time + time_per_step[leaf]

        current_time += 1

    print current_time - 1


# main(True)
main()
