#!/usr/bin/env python3
import re
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()

test_input = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def insert_tree(tree, path, obj):
    if not path:
        return
    head, tail = path[0:-1], path[-1]
    for p in head:
        if p not in tree:
            tree[p] = {}
        tree = tree[p]
    tree[tail] = obj
    return


def parse_tree(raw_input):
    lines = [s.strip() for s in raw_input.split('\n') if s.strip()]
    tree = {}
    path = []
    for line in lines:
        if m := re.match(r'\$ cd (.*)', line):
            dir = m.group(1)
            if dir == '/':
                path = []
            elif dir == '..':
                path.pop()
            else:
                path.append(dir)
        elif line == '$ ls':
            continue
        elif m := re.match(r'(\d+) (.+)', line):
            size, name = int(m.group(1)), m.group(2)
            insert_tree(tree, path + [name], {'_size': size})
        elif m := re.match('dir (.+)', line):
            name = m.group(1)
            insert_tree(tree, path + [name], {})
    return tree


def iter_dirs(tree):
    for k, v in tree.items():
        if k == '_size':
            continue
        if len(v) == 1:
            continue
        yield from iter_dirs(v)
        yield k, v


def part1(raw_input):
    tree = parse_tree(raw_input)
    fill_in_dir_sizes(tree)
    result = 0
    for k, v in iter_dirs(tree):
        if v['_size'] <= 100000:
            result += v['_size']
    return result


def part2(raw_input):
    tree = parse_tree(raw_input)
    fill_in_dir_sizes(tree)
    dirs = [(k, v['_size']) for k, v in iter_dirs(tree)]
    dirs = sorted(dirs, key=lambda d: d[1])

    current_unused_space = 70000000 - tree['_size']
    unused_space_missing = 30000000 - current_unused_space
    if unused_space_missing < 0:
        raise Exception("already done")

    for d, size in dirs:
        if size >= unused_space_missing:
            return size

    raise Exception("didn't find")


def fill_in_dir_sizes(tree):
    size = 0
    for k, v in tree.items():
        if k == '_size':
            continue
        fill_in_dir_sizes(v)
        size += v['_size']
    if '_size' not in tree:
        tree['_size'] = size
    return


def test_part1():
    # {'d' -> ({}, size)
    tree = parse_tree(test_input)
    fill_in_dir_sizes(tree)
    assert tree['a']['_size'] == 94853
    assert tree['a']['e']['_size'] == 584
    assert tree['d']['_size'] == 24933642
    assert tree['_size'] == 48381165
    assert part1(test_input) == 95437


def test_part2():
    assert part2(test_input) == 24933642


if __name__ == '__main__':
    print("Part 1: ", part1(input_text))
    print("Part 2: ", part2(input_text))
