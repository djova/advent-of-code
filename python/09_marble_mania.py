#!/usr/bin/env python
import re
from collections import defaultdict
from itertools import cycle, count
from os.path import join, realpath, dirname

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '09.txt')

test_examples = """\
9 players; last marble is worth 25 points; high score is 32
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.left = self
        self.right = self

    def insert_right(self, value):
        node = Node(value)
        node.left = self
        node.right = self.right
        node.right.left = node
        self.right = node
        return node

    def remove(self):
        self.left.right = self.right
        self.right.left = self.left
        return self.right

    def find(self, offset):
        next_node = self
        while offset != 0:
            next_node = next_node.left if offset < 0 else next_node.right
            offset = offset + 1 if offset < 0 else offset - 1
        return next_node

    def __str__(self):
        values = [self.value]
        node = self.right
        while node != self:
            values.append(node.value)
            node = node.right
        return ", ".join(map(str, values))


def calculate_score(num_players, last_marble_value):
    marbles = count(0, 1)
    scores = defaultdict(int)

    current_marble = None

    for player in cycle(range(num_players)):
        next_marble = marbles.next()
        if not current_marble:
            current_marble = Node(next_marble)
        elif next_marble % 23 == 0:
            scores[player] += next_marble
            to_remove = current_marble.find(-7)
            scores[player] += to_remove.value
            current_marble = to_remove.remove()
        else:
            current_marble = current_marble.find(1).insert_right(next_marble)

        if next_marble == last_marble_value:
            break

    return max(scores.values())


def validate_test_examples():
    for example in [e.strip() for e in test_examples.split('\n') if e.strip()]:
        num_players, last_marble_value, high_score = [int(i) for i in re.findall(r'\d+', example)]
        calculated_score = calculate_score(num_players, last_marble_value)
        if calculated_score != high_score:
            print "failed example '{}', calculated {} should be {}".format(example, calculated_score, high_score)


def main():
    num_players, last_marble_value = [int(i) for i in re.findall(r'\d+', open(input_file).read())]

    # part 1
    print calculate_score(num_players, last_marble_value)

    # part 2
    print calculate_score(num_players, last_marble_value * 100)


validate_test_examples()
main()
