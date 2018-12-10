#!/usr/bin/env python
import re
from collections import namedtuple, defaultdict
from itertools import chain
from os.path import join, realpath, dirname
from string import ascii_uppercase

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '08.txt')
test_input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

Node = namedtuple('Node', ['children', 'metadata'])


def load_input(test=False):
    raw = test_input if test else open(input_file).read()
    return [int(i) for i in raw.split()]


def build_tree(rest):
    header, rest = rest[0:2], rest[2:]
    num_children, num_metadata_entries = header
    children = []
    for _ in range(num_children):
        child, rest = build_tree(rest)
        children.append(child)

    metadata, rest = rest[:num_metadata_entries], rest[num_metadata_entries:]
    return Node(children, metadata), rest


def sum_metadata(tree):
    return sum(tree.metadata) + sum([sum_metadata(c) for c in tree.children])


def sum_indexed_metadata(tree):
    if not tree.children:
        return sum(tree.metadata)
    children = [tree.children[i-1] for i in tree.metadata if i != 0 and i-1 < len(tree.children)]
    return sum(sum_indexed_metadata(c) for c in children)


def main(test=False):
    nums = load_input(test)
    tree, _ = build_tree(nums)

    # part 1
    print sum_metadata(tree)

    # part 2
    print sum_indexed_metadata(tree)
    return


# main(True)
main()
