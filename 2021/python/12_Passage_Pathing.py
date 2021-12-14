#!/usr/bin/env python3
from collections import defaultdict, Counter
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '12.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

test_input2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

test_input3 = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

test_inputs = [
    test_input1,
    test_input2,
    test_input3,
]


def parse(raw):
    graph = defaultdict(set)
    for l in [l.strip() for l in raw.split("\n") if l.strip()]:
        k, v = l.split('-')
        graph[k].add(v)
        graph[v].add(k)
    return graph


class Tracker:
    def __init__(self, path):
        self.twice_done = False
        self.smalls = defaultdict(int)
        self.visit(*path)

    def can_visit(self, s):
        if s.isupper() or self.smalls[s] == 0:
            return True
        if self.smalls[s] > 0 and not self.twice_done and not s == 'start':
            return True
        return False

    def visit(self, *path):
        for s in path:
            if not self.can_visit(s):
                raise Exception("cannot visit")
            if not s.isupper():
                self.smalls[s] += 1
                if self.smalls[s] > 1:
                    self.twice_done = True


def navigate(graph, path):
    tracker = Tracker(path)
    other_paths = []
    while True:
        head = path[-1]
        if head == 'end':
            break
        valid_next_steps = [s for s in graph[head] if tracker.can_visit(s)]
        if not valid_next_steps:
            break
        head, rest = valid_next_steps[0], valid_next_steps[1:]
        for s in rest:
            other_paths.append(path + [s])
        path.append(head)
        tracker.visit(head)

    return path, other_paths


def find_paths(graph):
    pending = [['start']]
    finished = []
    while pending:
        path = pending.pop()
        path, other_paths = navigate(graph, path)
        if path[-1] == 'end':
            finished.append(path)
        pending.extend(other_paths)
    return len(finished)


print("running tests")
for i, t in enumerate(test_inputs):
    print("test ", i + 1, "paths", find_paths(parse(t)))

print("part 1", find_paths(parse(raw_input)))
