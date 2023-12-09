#!/usr/bin/env python3
from collections import Counter
from enum import Enum
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '07.txt')
input_text = open(input_file, 'r').read()


def parse_raw_input(raw_input):
    lines = [l.strip().split(' ') for l in raw_input.split('\n') if l.strip()]
    return [(Hand(hand), int(bid)) for hand, bid in lines]


cards = "AKQJT98765432"
card_strength = {c: i for i, c in enumerate(reversed(cards))}

cards_with_jokers = cards[0:cards.index('J')] + cards[cards.index('J') + 1:] + 'J'
card_strength_with_jokers = {c: i for i, c in enumerate(reversed(cards_with_jokers))}

JOKER_ENABLED = False

test_input = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


class HandRank(Enum):
    five_kind = 7
    four_kind = 6
    full_house = 5
    three_kind = 4
    two_pair = 3
    one_pair = 2
    high_card = 1

    def __lt__(self, other):
        return self.value < other.value


class Hand:
    def __init__(self, hand):
        self.hand = hand
        counts = Counter(self.hand)

        if len(counts) == 1:
            self.rank = HandRank.five_kind
        elif len(counts) == 2:
            self.rank = HandRank.full_house if 3 in counts.values() else HandRank.four_kind
        elif len(counts) == 3:
            self.rank = HandRank.three_kind if 3 in counts.values() else HandRank.two_pair
        elif len(counts) == 4:
            self.rank = HandRank.one_pair
        else:
            self.rank = HandRank.high_card

        if JOKER_ENABLED and 'J' in counts:
            if self.rank == HandRank.five_kind:
                return
            elif self.rank == HandRank.four_kind:
                self.rank = HandRank.five_kind
            elif self.rank == HandRank.full_house:
                self.rank = HandRank.five_kind
            elif self.rank == HandRank.three_kind:
                self.rank = HandRank.four_kind
            elif self.rank == HandRank.two_pair:
                if counts['J'] == 2:
                    self.rank = HandRank.four_kind
                else:
                    self.rank = HandRank.full_house
            elif self.rank == HandRank.one_pair:
                self.rank = HandRank.three_kind
            elif self.rank == HandRank.high_card:
                self.rank = HandRank.one_pair

    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        for self_c, other_c in zip(self.hand, other.hand):
            strengths = card_strength_with_jokers if JOKER_ENABLED else card_strength
            self_str, other_str = strengths[self_c], strengths[other_c]
            if self_str != other_str:
                return self_str < other_str


def winnings(raw_input):
    hands_bids = parse_raw_input(raw_input)
    hands_bids = sorted(hands_bids, key=lambda x: x[0])
    total_winnings = 0
    for rank, (hand, bid) in enumerate(hands_bids):
        rank = rank + 1
        winnings = rank * bid
        total_winnings += winnings
    return total_winnings


def test_winnings_part1():
    global JOKER_ENABLED
    JOKER_ENABLED = False
    hands_bids = sorted(parse_raw_input(test_input), key=lambda x: x[0])
    raw_hands = [h.hand for h, _ in hands_bids]
    assert raw_hands == ['32T3K', 'KTJJT', 'KK677', 'T55J5', 'QQQJA']
    assert winnings(test_input) == 6440


def test_winnings_part2():
    global JOKER_ENABLED
    JOKER_ENABLED = True
    hands_bids = parse_raw_input(test_input)
    for h, _ in hands_bids:
        h.joker_enabled = True
    hands_bids = sorted(hands_bids, key=lambda x: x[0])
    raw_hands = [h.hand for h, _ in hands_bids]
    assert raw_hands == ['32T3K', 'KK677', 'T55J5', 'QQQJA', 'KTJJT']
    assert winnings(test_input) == 5905


def run_main():
    global JOKER_ENABLED
    JOKER_ENABLED = False
    print("part 1:", winnings(input_text))
    JOKER_ENABLED = True
    print("part 2:", winnings(input_text))


if __name__ == '__main__':
    run_main()
