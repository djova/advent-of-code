#!/usr/bin/env python3
from collections import defaultdict
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


def navigate(graph, path):
    visited_small = set([x for x in path if not x.isupper()])
    other_paths = []
    while True:
        head = path[-1]
        valid_next_steps = [n for n in graph[head] if n not in visited_small]
        if not valid_next_steps:
            break
        head, rest = valid_next_steps[0], valid_next_steps[1:]
        for s in rest:
            other_paths.append(path + [s])
        path.append(head)
        if not head.isupper():
            visited_small.add(head)
        if head == 'end':
            break

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
