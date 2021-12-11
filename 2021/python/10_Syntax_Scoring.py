#!/usr/bin/env python3
from collections import Counter
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '10.txt')
raw_input = open(input_file, 'r').read()

test_input1 = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

invalid_scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

completion_scores = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

open_to_close = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}


def parse(raw):
    return [list(s.strip()) for s in raw.split("\n") if s.strip()]


def calculate_score(lines):
    invalids = []
    completions = []
    for line in lines:
        pending = []
        invalid_closing_char = None

        for c in line:
            if c in open_to_close:
                pending.append(c)
                continue
            if c in invalid_scores:
                if c == open_to_close[pending[-1]]:
                    pending.pop()
                    continue
                invalid_closing_char = c
                break
            raise Exception("impossible")

        if invalid_closing_char:
            invalids.append(invalid_closing_char)
            continue

        completion = []
        completion_score = 0
        while pending:
            c = open_to_close[pending.pop()]
            completion.append(c)
            completion_score *= 5
            completion_score += completion_scores[c]

        completions.append((''.join(completion), completion_score))

    invalid_counts = Counter(invalids)
    score_per_char = {c: invalid_scores[c] * n for c, n in invalid_counts.items()}
    score = sum(score_per_char.values())

    completions = sorted(completions, key=lambda x: x[1])
    midpoint = completions[int(len(completions) / 2)]

    return f"{invalid_counts} - sum: {score}. mid_completion: {midpoint}"


print(calculate_score(parse(test_input1)))
print(calculate_score(parse(raw_input)))
