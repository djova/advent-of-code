import math

ADD = 1
MULT = 2
SAVE_TO = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
HALT = 99

num_params = {
    ADD: 3,
    MULT: 3,
    SAVE_TO: 1,
    OUTPUT: 1,
    JUMP_IF_TRUE: 2,
    JUMP_IF_FALSE: 2,
    LESS_THAN: 3,
    EQUALS: 3
}

# parameter modes

# value = value at address
POSITION_MODE = 0

# plain value
IMMEDIATE_MODE = 1


def extract_param_modes(instruction, num_params):
    for exp in range(2, num_params + 2):
        yield math.floor(instruction % (10 ** (exp + 1)) / 10 ** exp)


def parse_instruction(instruction):
    opcode = instruction % 100
    param_modes = list(extract_param_modes(instruction, num_params[opcode]))
    return opcode, param_modes


class Intcode:
    def __init__(self, memory, input=0):
        self.memory = memory.copy()
        self.input = input
        self.pi = 0

    def extract_params(self, param_modes, last_immediate=False):
        for i, mode in enumerate(param_modes):
            p_index = self.pi + i + 1
            val = self.memory[p_index]
            if last_immediate and i == len(param_modes) - 1:
                yield val
            elif mode == POSITION_MODE:
                yield self.memory[val]
            elif mode == IMMEDIATE_MODE:
                yield val
            else:
                raise Exception("unknown mode: {}".format(mode))

    def run(self):
        while (instruction := self.memory[self.pi]) != HALT:
            opcode, param_modes = parse_instruction(instruction)
            if opcode == ADD:
                a, b, result_i = list(self.extract_params(param_modes, True))
                self.memory[result_i] = a + b
                self.pi += 4
            elif opcode == MULT:
                a, b, result_i = list(self.extract_params(param_modes, True))
                self.memory[result_i] = a * b
                self.pi += 4
            elif opcode == SAVE_TO:
                result_i = self.memory[self.pi + 1]
                self.memory[result_i] = self.input
                self.pi += 2
            elif opcode == OUTPUT:
                params = list(self.extract_params(param_modes))
                print(params[0])
                self.pi += 2
            elif opcode == JUMP_IF_TRUE:
                a, b = list(self.extract_params(param_modes))
                if a != 0:
                    self.pi = b
                else:
                    self.pi += 3
            elif opcode == JUMP_IF_FALSE:
                a, b = list(self.extract_params(param_modes))
                if a == 0:
                    self.pi = b
                else:
                    self.pi += 3
            elif opcode == LESS_THAN:
                a, b, result_i = list(self.extract_params(param_modes, True))
                self.memory[result_i] = 1 if a < b else 0
                self.pi += 4
            elif opcode == EQUALS:
                a, b, result_i = list(self.extract_params(param_modes, True))
                self.memory[result_i] = 1 if a == b else 0
                self.pi += 4
            else:
                raise Exception("unknown opcode: {}".format(opcode))
