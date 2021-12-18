#!/usr/bin/env python3
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
        self.stack = []
        self.version_sum = 0
        self.literals = []
        self.sub_bits_left = None
        self.sub_packets_left = None

    def consume(self, n):
        result = self.raw[self.i:self.i + n]
        self.i += n
        if self.sub_bits_left is not None:
            self.sub_bits_left -= n
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
        print(f"literal={literal}")
        self.literals.append(literal)
        return literal

    def consume_operator(self):
        length_type_id = self.consume(1)
        # return: sub_bits, sub_count
        if length_type_id == '0':
            return binary_s_to_int(self.consume(15)), None
        else:
            return None, binary_s_to_int(self.consume(11))

    def packet_done(self):
        if self.sub_bits_left is not None:
            self.sub_bits_left -= 1

    def finished(self):
        if (self.end_i - self.i) < 4 and set(self.raw[self.i:]) == {"0"}:
            print("consuming residual zeros", self.raw[self.i:])
            return True
        if self.sub_bits_left is not None and self.sub_bits_left == 0:
            print("sub bits done")
            return True
        if self.sub_packets_left is not None and self.sub_packets_left == 0:
            print("sub bits done")
            return True
        return False

    def parse(self):
        while self.i < self.end_i and not self.finished():
            version = binary_s_to_int(self.consume(3))
            type_id = binary_s_to_int(self.consume(3))
            self.version_sum += version
            print(f"version={version}, type_id={type_id}")

            if type_id == 4:
                self.consume_literal()
                self.packet_done()
                continue

            sub_bits, sub_count = self.consume_operator()
            if self.sub_bits_left is None and self.sub_packets_left is None:
                self.sub_bits_left = sub_bits
                self.sub_packets_left = sub_count
                print(f"starting sub packet. bits={sub_bits} count={sub_count}")
            else:
                print("starting sub-sub packet")
            self.packet_done()


def go(raw):
    print("\n----  new transmission ----")
    parser = Parser(raw)
    parser.parse()
    return f"version_sum={parser.version_sum} literals={parser.literals}"


print("test - expecting literals: 2021 |", go(parse("D2FE28")))
print("test - expecting literals: 10, 20 |", go(parse("38006F45291200")))
print("test - expecting literals: 1, 2, 3 |", go(parse("EE00D40C823060")))
print("test - expecting version_sum=16 |", go(parse("8A004A801A8002F478")))
print("test - expecting version_sum=12 |", go(parse("620080001611562C8802118E34")))
print("test - expecting version_sum=23 |", go(parse("C0015000016115A2E0802F182340")))
print("test - expecting version_sum=31 |", go(parse("A0016C880162017C3686B18A3D4780")))
print("part 1", go(parse(raw_input)))
