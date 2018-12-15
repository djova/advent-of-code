#!/usr/bin/env python
from os.path import join, dirname, realpath

input_file = join(dirname(realpath(__file__)), '..', 'inputs', '12.txt')

test_input = """\
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""


def load_input(test=False):
    raw = test_input if test else open(input_file).read()
    lines = [l for l in raw.split('\n') if l]
    header, rest = lines[0], lines[1:]
    initial_state = header[len("initial state: "):]
    rules = dict(r.split(' => ') for r in rest)
    return initial_state, rules


class Simulation:
    def __init__(self, initial_state, rules):
        self.state = initial_state
        self.rules = rules

        self.front_pad = 0
        self.empty_pad = '.....'
        self.repeat_size = 10
        self.queue = []
        self.repeat_found = False
        self.current_generation = 0

    def pad_state(self):
        if not self.state.startswith(self.empty_pad):
            self.state = self.empty_pad + self.state
            self.front_pad += len(self.empty_pad)
        if not self.state.endswith(self.empty_pad):
            self.state = self.state + self.empty_pad

    def append_queue(self):
        if len(self.queue) == self.repeat_size:
            self.queue.pop(0)
        self.queue.append((self.current_generation, self.front_pad, self.state))

    def queue_repeats(self):
        if len(self.queue) < self.repeat_size:
            return False
        states = [s for g, p, s in self.queue]
        head, tail = states[0:len(states) / 2], states[len(states) / 2:]
        return all([a == b for a, b in zip(head, tail)])

    def next_generation(self):
        self.pad_state()
        self.state = ''.join([self.rules.get(self.state[i:i + 5], '.') for i in xrange(len(self.state) - 5)])
        self.front_pad -= 2
        self.current_generation += 1
        if not self.repeat_found:
            self.append_queue()
            self.repeat_found = self.queue_repeats()
            if self.repeat_found:
                self.queue = self.queue[len(self.queue) / 2:]

    def predict_generation(self, generation):
        last_index = len(self.queue) - 1
        last_gen, last_front_pad, last_state = self.queue[last_index]
        remaining_generations = max(0, generation - last_gen)
        _, end_front_pad, end_state = self.queue[(last_index + remaining_generations) % len(self.queue)]
        num_loops = remaining_generations / len(self.queue) + 1
        adjusted_end_front_pad = end_front_pad - 5 * num_loops
        return adjusted_end_front_pad, end_state

    def predict_current_generation(self):
        end_front_pad, end_state = self.predict_generation(self.current_generation)
        if end_state != self.state:
            print "predicted wrong state: {} != {}".format(end_state, self.state)
        if end_front_pad != self.front_pad:
            print "predicted wrong front_pad: {} != {}".format(end_front_pad, self.front_pad)
        return end_front_pad, end_state

    def get_pot_sum(self):
        return sum([i - self.front_pad for i, c in enumerate(self.state) if c == '#'])


def run_generations(initial_state, rules, target_generation, test_predict=False):
    sim = Simulation(initial_state, rules)
    while sim.current_generation < target_generation:
        if sim.repeat_found:
            if test_predict:
                sim.predict_current_generation()
            else:
                break
        sim.next_generation()

    if sim.current_generation < target_generation:
        end_front_pad, end_state = sim.predict_generation(target_generation)
        sim.front_pad = end_front_pad
        sim.state = end_state

    return sim.get_pot_sum()


def run_tests():
    initial_state, rules = load_input(True)

    expected_pot_sum = 325
    pot_sum = run_generations(initial_state, rules, 20)
    if pot_sum == expected_pot_sum:
        print "correct potsum"
    else:
        print "wrong potsum {} != {}".format(pot_sum, expected_pot_sum)

    run_generations(initial_state, rules, 10000, True)
    return


def main():
    initial_state, rules = load_input()

    # part 1
    pot_sum = run_generations(initial_state, rules, 20)
    print pot_sum

    # part 2
    pot_sum = run_generations(initial_state, rules, int(50e9))
    print pot_sum

    return


run_tests()
# main()
