#!/usr/bin/env python3
import math
from collections import defaultdict, Counter
from os.path import join, dirname, realpath

import itertools
import re

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '21.txt')
raw_input = open(input_file, 'r').read()

test_input = """\
Player 1 starting position: 4
Player 2 starting position: 8
"""


def parse(raw):
    lines = [[int(i) for i in re.findall(r"-?\d+", l)] for l in raw.split("\n") if l.strip()]
    return lines[0][1], lines[1][1]


def roll(die, times=3):
    result = 0
    while times > 0:
        if die > 100:
            die = 1
        times -= 1
        result += die
        die += 1
    return die, result


def move(p1, steps):
    p1 = (p1 + steps) % 10
    return 10 if p1 == 0 else p1


def part1(p1, p2, max_score=1000):
    die = 1
    p1_score, p2_score = 0, 0
    die_rolls = 0
    while True:
        die, p1_steps = roll(die)
        die_rolls += 3
        p1 = move(p1, p1_steps)
        p1_score += p1
        if p1_score >= max_score:
            break

        die, p2_steps = roll(die)
        die_rolls += 3
        p2 = move(p2, p2_steps)
        p2_score += p2
        if p2_score >= max_score:
            break

    winner = "p1" if p1_score > max_score else "p2"
    losing_score = min(p1_score, p2_score)

    print(f"game ended. p1_score={p1_score} p2_score={p2_score} winner={winner} die_rolls={die_rolls} loser*die={losing_score * die_rolls}")


def iter_state(state, roll_states):
    result = defaultdict(int)
    for scores, ac in state.items():
        for roll_sum, bc in roll_states.items():
            p_score, pos = scores[-2]
            pos = move(pos, roll_sum)
            p_score += pos
            next_scores = scores[1:] + ((p_score, pos),)
            result[next_scores] += bc * ac
    return result


def part2(p1, p2):
    print(f"running part2 p1={p1} p2={p2}")
    round = 0
    roll_states = Counter(sum(c) for c in itertools.product((1, 2, 3), repeat=3))

    state = {((0, p1), (0, p2)): 1}
    p1_wins, p2_wins = 0, 0
    while state:
        state = iter_state(state, roll_states)
        done_keys = set()
        for key, n in state.items():
            p_score, _ = key[-1]
            if p_score >= 21:
                if round % 2 == 0:
                    p1_wins += n
                else:
                    p2_wins += n
                done_keys.add(key)
        for k in done_keys:
            del state[k]

        print(f"round {round} len(state)={len(state)} len(don_keys)={len(done_keys)}")

        round += 1

    who_has_more = "p1" if p1_wins > p2_wins else "p2"
    print(f"states exhausted. p1_wins={p1_wins} p2_wins={p2_wins}. more: {who_has_more}")


# part1(*parse(test_input))
# print("running main")
# part1(*parse(raw_input))
print("test part2")
part2(*parse(test_input))
part2(*parse(raw_input))
