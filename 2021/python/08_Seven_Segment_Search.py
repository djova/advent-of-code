#!/usr/bin/env python3
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '08.txt')
raw_input = open(input_file, 'r').read()

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

test_input1 = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""


def parse(raw):
    result = []
    for line in raw.split("\n"):
        values = [s.strip() for s in line.replace("|", "").split() if s.strip()]
        values = ["".join(sorted(s)) for s in values]
        signals, output = values[0:10], values[10:14]
        result.append((signals, output))
    return result


digit_mappings = {
    1: "cf",  # len 2
    7: "acf",  # len 3
    4: "bcdf",  # len 4
    2: "acdeg",  # len 5
    3: "acdfg",
    5: "abdfg",
    0: "abcefg",  # len 6
    6: "abdefg",
    9: "abcdfg",
    8: "abcdefg",  # len 7
}

len_to_d = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}


def detect(entries):
    unique_segment_appearances = 0
    total_sum = 0
    for signals, output in entries:
        dmap = {len_to_d[len(s)]: set(s) for s in signals if len(s) in len_to_d}

        osum = 0
        for o in output:
            osum *= 10
            o = set(o)
            if d := len_to_d.get(len(o), None):
                osum += d
                unique_segment_appearances += 1
                continue
            if len(o) == 5:
                # one of 2, 3, 5
                if len(dmap[1] & o) == 2:
                    osum += 3
                elif len(dmap[4] & o) == 2:
                    osum += 2
                else:
                    osum += 5
            elif len(o) == 6:
                # one of 0, 6, 9
                if len(dmap[1] & o) == 1:
                    osum += 6
                elif len(dmap[4] & o) == 4:
                    osum += 9
                else:
                    dmap[0] = o
            else:
                raise Exception("wah")
        total_sum += osum

    return f"num unique segment appeared: {unique_segment_appearances}, total sum: {total_sum}"


print("Part 1 (test): ", detect(parse(test_input1)))
print("Part 1: ", detect(parse(raw_input)))
