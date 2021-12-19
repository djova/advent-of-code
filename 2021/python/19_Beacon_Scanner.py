#!/usr/bin/env python3
import math
from collections import defaultdict, Counter
from os.path import join, dirname, realpath

import itertools
import re

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '19.txt')
raw_input = open(input_file, 'r').read()

test_input_1 = """\
--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 1 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 2 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 3 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 4 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8
"""

test_input_2 = """\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
"""


def parse(raw):
    scanners = defaultdict(list)
    current_scanner = None
    for line in raw.split("\n"):
        if not line.strip():
            continue
        ints = tuple([int(s) for s in re.findall(r"-?\d+", line)])
        if len(ints) == 1:
            current_scanner = ints[0]
            continue
        scanners[current_scanner].append(ints)
    return {s: set(points) for s, points in scanners.items()}


def gen_mults():
    flips = set()
    flips.add((1, 1, 1))
    flips.add((-1, -1, -1))
    flips.update(itertools.permutations((-1, 1, 1)))
    flips.update(itertools.permutations((-1, -1, 1)))
    return flips


mults = gen_mults()

swaps = [
    # passthrough
    lambda x, y, z: (x, y, z),
    # swap 2
    lambda x, y, z: (y, x, z),
    lambda x, y, z: (x, z, y),
    lambda x, y, z: (z, y, x),
    # rotate all 3
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (y, z, x),
]


def mult_point(p, r):
    return tuple(a * b for a, b in zip(r, p))


def flip_n_swap(points, m, f):
    return set(mult_point(f(*p), m) for p in points)


def swap_points(points, f):
    return set(f(*p) for p in points)


def translate(points, t):
    return set(tuple(a + b for a, b in zip(p, t)) for p in points)


def sub(p1, p2):
    # p1 - p2
    return tuple(a - b for a, b in zip(p1, p2))


def translations(s1, s2):
    yield 0, 0, 0
    for p1 in s1:
        for p2 in s2:
            t = sub(p1, p2)
            yield t


def transformations():
    for m in mults:
        for f in swaps:
            yield m, f


def find_translation(s1, s2, min_overlap=12):
    # from s2 -> s1
    # s1_dist, s2_dist = distances(s1), distances(s2)
    # if len(s1_dist & s2_dist) < min_overlap:
    #     return None, None, None, None
    for m, f in transformations():
        s2_f = flip_n_swap(s2, m, f)
        for t in translations(s1, s2_f):
            s2_t = translate(s2_f, t)
            overlap = s1 & s2_t
            if len(overlap) >= min_overlap:
                return f, t, s2_t, overlap

    return None, None, None, None


def find_beacons_reduce_approach(scanners):
    beacons = scanners[0]
    scanners_coords = [(0, 0)]
    remaining = set(scanners.keys())
    remaining.remove(0)
    while remaining:
        print("find_beacons_reduce_approach loop start")
        for i in list(remaining):
            if i not in remaining:
                continue
            print(f"finding overlap for i={i}")
            f, t, s2_t, overlap = find_translation(beacons, scanners[i])
            if not overlap:
                print(f"no overlap for i={i}")
                continue
            print(f"found overlap for i={i}")
            beacons = beacons | s2_t
            scanners_coords.append(t)
            remaining.remove(i)
    return beacons, scanners_coords


def manhattan_distance(v1, v2):
    return sum(abs(a - b) for a, b in zip(v1, v2))


def max_manhattan_distance(beacons):
    max_distance = 0
    max_a, max_b = None, None
    for a, b in itertools.combinations(list(beacons), 2):
        d = manhattan_distance(a, b)
        if d > max_distance:
            max_distance = d
            max_a, max_b = a, b
    return max_distance, max_a, max_b


def run_test():
    print("testing same scanner multiple orientations")
    scanners = parse(test_input_1)
    for i in range(1, len(scanners.keys())):
        f, t, s2_t, overlap = find_translation(scanners[0], scanners[i], min_overlap=6)
        assert t == (0, 0, 0)
        assert len(overlap) == 6

    print("doing test1")
    scanners = parse(test_input_2)
    f, t, s2_t, overlap = find_translation(scanners[0], scanners[1])

    assert len(overlap) == 12
    assert t == (68, -1246, -43)

    f, t, s2_t, overlap = find_translation(scanners[1], scanners[4])
    assert len(overlap) == 12

    beacons, scanner_coords = find_beacons_reduce_approach(scanners)
    print(f"test1 beacons expected=79: {len(beacons)}")
    print(f"done test1, maxm {max_manhattan_distance(scanner_coords)}")


# run_test()

print("running main")
beacons, scanner_coords = find_beacons_reduce_approach(parse(raw_input))
print(f"found beacons: {len(beacons)}, maxm: {max_manhattan_distance(scanner_coords)}")
