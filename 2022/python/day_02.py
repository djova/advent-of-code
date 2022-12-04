#!/usr/bin/env python3
import re
from os.path import join, dirname, realpath, basename

day_str = re.match(r'day_(\d+).py', basename(__file__)).group(1)
input_file = join(dirname(realpath(__file__)), '..', 'inputs', f'{day_str}.txt')
input_text = open(input_file, 'r').read()

test_input_text = """\
A Y
B X
C Z
"""

opponent_moves = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors'
}

my_moves = {
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors'
}

move_scores = {
    'rock': 1,
    'paper': 2,
    'scissors': 3
}

move_wins = {
    'scissors': 'paper',
    'paper': 'rock',
    'rock': 'scissors'
}

move_losses = {v: k for k, v in move_wins.items()}


def rock_paper_scissors(a, b):
    if a == b:
        return False, False
    if move_wins[a] == b:
        return True, False
    return False, True


def part1(strategy):
    score = 0
    for opponent_move, my_move in strategy:
        opponent_move, my_move = opponent_moves[opponent_move], my_moves[my_move]
        opponent_win, me_win = rock_paper_scissors(opponent_move, my_move)
        round_score = move_scores[my_move]
        if me_win:
            round_score += 6
        elif opponent_win:
            round_score += 0
        else:
            round_score += 3
        score += round_score
    return score


def part2(strategy):
    score = 0
    for opponent_move, round_end in strategy:
        opponent_move = opponent_moves[opponent_move]
        round_score = 0
        if round_end == 'X':
            # lose
            my_move = move_wins[opponent_move]
            round_score += move_scores[my_move]
        elif round_end == 'Y':
            # draw
            round_score += move_scores[opponent_move] + 3
        else:
            # win
            my_move = move_losses[opponent_move]
            round_score += move_scores[my_move] + 6
        score += round_score

    return score


def process_raw_input(raw_input):
    for line in raw_input.split('\n'):
        line = line.strip()
        if line:
            yield line.split()


test_strategy = list(process_raw_input(test_input_text))
input_strategy = list(process_raw_input(input_text))


def test_part1():
    assert part1(test_strategy) == 15


def test_part2():
    assert part2(test_strategy) == 12


print("Part 1: ", part1(input_strategy))
print("Part 2: ", part2(input_strategy))
