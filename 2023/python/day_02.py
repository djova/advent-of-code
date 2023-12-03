#!/usr/bin/env python3
import functools
import re
from collections import defaultdict
from os.path import join, dirname, realpath

import pytest

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '02.txt')
input_text = open(input_file, 'r').read()


def combine_cube_sets(a, b, aggr_func):
    combined = defaultdict(int)
    for cube_set in [a, b]:
        for color, count in cube_set.items():
            combined[color] = aggr_func(combined[color], count)
    return combined


def filter_possible_games(games, cubes):
    for game_id, cube_sets in games:
        combined = functools.reduce(
            functools.partial(combine_cube_sets, aggr_func=max),
            cube_sets,
            defaultdict(int)
        )
        if all([combined[color] <= cubes[color] for color in cubes]):
            yield game_id, combined


def get_game_powers(games):
    for game_id, cube_sets in games:
        combined = functools.reduce(
            functools.partial(combine_cube_sets, aggr_func=max),
            cube_sets,
            defaultdict(int)
        )
        yield game_id, functools.reduce(lambda a, b: a * b, combined.values())


def parse_raw_input(raw_input):
    for line in raw_input.split('\n'):
        line = line.strip()
        if not line:
            continue
        game_prefix, cubes = line.split(':')
        game_id = int(game_prefix.split(' ')[1])
        cube_sets = []
        for raw_cube_set in cubes.split(';'):
            cube_set = {}
            for raw_cube in raw_cube_set.split(','):
                raw_cube = raw_cube.strip()
                if not raw_cube:
                    continue
                count, color = raw_cube.split(' ')
                cube_set[color] = int(count)
            cube_sets.append(cube_set)
        yield game_id, cube_sets

    return []


test_input = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def test_possible_games():
    games = parse_raw_input(test_input)
    possible = list(filter_possible_games(games, {
        'red': 12,
        'green': 13,
        'blue': 14,
    }))
    assert len(possible) == 3
    assert sum([game_id for game_id, _ in possible]) == 8


@pytest.mark.parametrize("game_id,power", [
    (1, 48),
    (2, 12),
    (3, 1560),
    (4, 630),
    (5, 36),
])
def test_game_powers(game_id, power):
    games = parse_raw_input(test_input)
    game_powers = {game_id: power for game_id, power in get_game_powers(games)}
    assert game_powers[game_id] == power


def test_total_power():
    games = parse_raw_input(test_input)
    power_sum = sum(power for _, power in get_game_powers(games))
    assert power_sum == 2286


def run_main():
    games = list(parse_raw_input(raw_input=input_text))
    possible = list(filter_possible_games(games, {
        'red': 12,
        'green': 13,
        'blue': 14,
    }))
    print("part 1:", sum([game_id for game_id, _ in possible]))

    total_power = sum(power for _, power in get_game_powers(games))
    print("part 2:", total_power)


if __name__ == '__main__':
    run_main()
