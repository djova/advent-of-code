#!/usr/bin/env python3
import itertools
from os.path import join, dirname, realpath

from lib.intcode import Intcode

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '08.txt')
input_ints = [int(i) for i in open(input_file, 'r').read().strip()]


def split_layers(ints, chunk_size):
    num_layers = int(len(ints) / chunk_size)
    for i in range(num_layers):
        yield ints[chunk_size * i:chunk_size * (i + 1)]


image_width = 25
image_height = 6

raw_layers = list(split_layers(input_ints, image_width * image_height))
num_layers = len(raw_layers)
min_l = min(raw_layers, key=lambda l: l.count(0))
print(min_l.count(1) * min_l.count(2))

rows = [[] for _ in range(image_height)]
for layer in raw_layers:
    for i, row in enumerate(split_layers(layer, image_width)):
        rows[i].append(row)


def render(pixel_layers):
    for pixel in pixel_layers:
        if pixel == 0:
            return 0
        elif pixel == 1:
            return 1
        elif pixel == 2:
            continue
    return 2


for row in rows:
    print(' '.join([str(render(x)) for x in zip(*row)]))
