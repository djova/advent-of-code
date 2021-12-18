#!/usr/bin/env python3
from functools import reduce
from os.path import join, dirname, realpath

import heapq
from builtins import int

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '16.txt')
raw_input = open(input_file, 'r').read()

hex_mapping = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def parse(raw):
    return ''.join([hex_mapping[c] for c in raw.strip()])


def binary_s_to_int(raw):
    result = 0
    for i, c in enumerate(reversed(raw)):
        if c == '1':
            result += 2 ** i
    return result


class Parser:
    def __init__(self, raw):
        self.raw = raw
        self.i = 0
        self.end_i = len(raw) - 1
        self.version_sum = 0
        self.literals = []

    def consume(self, n):
        result = self.raw[self.i:self.i + n]
        self.i += n
        return result

    def consume_literal(self):
        binary_s = ""
        while self.i < self.end_i:
            chunk = self.consume(5)
            if chunk[0] == '1':
                binary_s += chunk[1:]
                continue
            else:
                binary_s += chunk[1:]
                break

        literal = binary_s_to_int(binary_s)
        self.literals.append(literal)
        return literal

    def consume_operator(self):
        length_type_id = self.consume(1)
        if length_type_id == '0':
            return binary_s_to_int(self.consume(15)), None
        else:
            return None, binary_s_to_int(self.consume(11))

    def parse_packet(self, debug=False):
        version = binary_s_to_int(self.consume(3))
        type_id = binary_s_to_int(self.consume(3))
        self.version_sum += version
        if debug:
            print(f"starting-packet i={self.i} remaining_i={self.end_i - self.i} version={version} type_id={type_id}")

        if type_id == 4:
            literal = self.consume_literal()
            if debug:
                print(f"finished-packet literal={literal}")
            return literal

        values = []
        bits, packets = self.consume_operator()
        if bits:
            end_i = self.i + bits
            while self.i < end_i:
                values.append(self.parse_packet())
        else:
            for _ in range(packets):
                values.append(self.parse_packet())

        if type_id == 0:
            return sum(values)
        elif type_id == 1:
            return reduce(lambda a, b: a * b, values)
        elif type_id == 2:
            return min(values)
        elif type_id == 3:
            return max(values)
        elif type_id == 5:
            return 1 if values[0] > values[1] else 0
        elif type_id == 6:
            return 1 if values[0] < values[1] else 0
        elif type_id == 7:
            return 1 if values[0] == values[1] else 0


def go(raw):
    print("\n----  new transmission ----")
    parser = Parser(raw)
    value = parser.parse_packet()
    return f"version_sum={parser.version_sum} literals={parser.literals} value={value}"


print("test - expecting literals: 2021 |", go(parse("D2FE28")))
print("test - expecting literals: 10, 20 |", go(parse("38006F45291200")))
print("test - expecting literals: 1, 2, 3 |", go(parse("EE00D40C823060")))
print("test - expecting version_sum=16 |", go(parse("8A004A801A8002F478")))
print("test - expecting version_sum=12 |", go(parse("620080001611562C8802118E34")))
print("test - expecting version_sum=23 |", go(parse("C0015000016115A2E0802F182340")))
print("test - expecting version_sum=31 |", go(parse("A0016C880162017C3686B18A3D4780")))
print("test - expecting value=3 |", go(parse("C200B40A82")))
print("test - expecting value=54 |", go(parse("04005AC33890")))
print("test - expecting value=7 |", go(parse("880086C3E88112")))
print("test - expecting value=9 |", go(parse("CE00C43D881120")))
print("test - expecting value=1 |", go(parse("9C0141080250320F1802104A08")))
print("part 1", go(parse(raw_input)))
