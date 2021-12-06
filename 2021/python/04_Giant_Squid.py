#!/usr/bin/env python3
from os.path import join, dirname, realpath
import re
import itertools

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '04.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class BingoBoard:
    def __init__(self, rows):
        self.rows = [[(i, False) for i in row] for row in rows]
        self.index = {}
        for x, row in enumerate(self.rows):
            for y, (n, _) in enumerate(row):
                self.index[n] = (x, y)

    def mark(self, n):
        if n in self.index:
            row, col = self.index[n]
            if self.rows[row][col][0] != n:
                raise Exception("index error")
            self.rows[row][col] = (n, True)

    def columns(self):
        for col in range(len(self.rows)):
            yield [self.rows[row][col] for row in range(len(self.rows))]

    def won(self):
        for row in self.rows:
            if all(m for _, m in row):
                return True
        for column in self.columns():
            if all(m for _, m in column):
                return True
        return False

    def unmarked(self):
        for row in self.rows:
            for n, m in row:
                if not m:
                    yield n


def parse(raw):
    intlines = []
    for line in raw.split("\n"):
        if not line.strip():
            continue
        intlines.append([int(x) for x in re.findall(r"\d+", line)])

    numbers, rest = intlines[0], intlines[1:]
    boards = [BingoBoard(rest[i:i + 5]) for i in range(0, len(rest), 5)]

    return numbers, boards


def part_1(raw):
    numbers, boards = parse(raw)
    for n in numbers:
        for i, b in enumerate(boards):
            b.mark(n)
            if b.won():
                score = n * sum(b.unmarked())
                return f"board {i + 1} won with score {score}"
    return "no board won"


print("Part 1 (test): ", part_1(test_input1))
print("Part 1: ", part_1(raw_input))


def part_2(raw):
    numbers, boards = parse(raw)
    winners = set()
    for n in numbers:
        for i, b in enumerate(boards):
            if i in winners:
                continue
            b.mark(n)
            if b.won():
                winners.add(i)
                score = n * sum(b.unmarked())
                if len(winners) == len(boards):
                    return f"board {i + 1} won last with score {score}"
    return "all numbers used and no board won"


print("Part 2 (test): ", part_2(test_input1))
print("Part 2: ", part_2(raw_input))
