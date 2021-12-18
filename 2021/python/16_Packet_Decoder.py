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
        self.version_sum = 0
        self.literals = []
        self.stack = []

    def consume(self, n):
        result = self.raw[self.i:self.i + n]
        self.i += n
        return result

    def finished(self):
        if self.i >= self.end_i:
            print("done")
            return True
        if (self.end_i - self.i) < 4 and set(self.raw[self.i:]) == {"0"}:
            print("consuming residual zeros", self.raw[self.i:])
            return True

        # pop finished
        while self.stack:
            state = self.stack[-1]
            consumed = self.i - state['start_i']
            if 'bits' in state and consumed >= state['bits']:
                print(f"subpacket done (bits)")
                self.stack.pop()
            elif 'packets' in state and state['packets'] == 0:
                self.stack.pop()
                print(f"subpacket done (bits)")
            else:
                break

        if not self.stack:
            return True

        state = self.stack[-1]
        if 'packets' in state:
            state['packets'] -= 1

        remaining_i = self.end_i - self.i
        print(f"> packet_state={state} len(stack)={len(self.stack)} remaining_i={remaining_i}")

        return False

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

    def start_packet(self, sub_bits, sub_packets):
        print(f"starting sub packet (bits,packets)={(sub_bits, sub_packets)}")
        state = {
            'start_i': self.i,
        }
        if sub_bits:
            state['bits'] = sub_bits
        if sub_packets:
            state['packets'] = sub_packets
        self.stack.append(state)

    def parse(self):
        self.start_packet(None, 1)
        while not self.finished():
            version = binary_s_to_int(self.consume(3))
            type_id = binary_s_to_int(self.consume(3))
            self.version_sum += version
            print(f"version={version}, type_id={type_id}")

            if type_id == 4:
                self.consume_literal()
                continue

            sub_bits, sub_count = self.consume_operator()
            if not sub_bits and not sub_count:
                raise Exception("empty sub packet")
            self.start_packet(sub_bits, sub_count)


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
