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

# operation I/O => (num_inputs, num_outputs)
op_io = {
    ADD: (2, 1),
    MULT: (2, 1),
    SAVE_TO: (0, 1),
    OUTPUT: (1, 0),
    JUMP_IF_TRUE: (2, 0),
    JUMP_IF_FALSE: (2, 0),
    LESS_THAN: (2, 1),
    EQUALS: (2, 1)
}

# parameter modes

# value = value at address
POSITION_MODE = 0

# plain value
IMMEDIATE_MODE = 1


def extract_param_modes(instruction, op_io):
    for exp in range(2, op_io + 2):
        yield math.floor(instruction % (10 ** (exp + 1)) / 10 ** exp)


class Intcode:
    def __init__(self, memory, input=0):
        self.memory = memory.copy()
        self.input = input
        self.pi = 0

    def extract_params(self, param_modes):
        for i, mode in enumerate(param_modes):
            val = self.memory[self.pi + i + 1]
            if mode == POSITION_MODE:
                yield self.memory[val]
            elif mode == IMMEDIATE_MODE:
                yield val
            else:
                raise Exception("unknown mode: {}".format(mode))

    def parse_instruction(self, instruction):
        opcode = instruction % 100
        n_in, n_out = op_io[opcode]
        param_modes = list(extract_param_modes(instruction, n_in))
        in_params = list(self.extract_params(param_modes))
        out_i = self.pi + n_in + 1
        out_params = self.memory[out_i:out_i + n_out]
        return opcode, in_params + out_params

    def run(self):
        while (instruction := self.memory[self.pi]) != HALT:
            opcode, params = self.parse_instruction(instruction)
            jumped = False
            if opcode == ADD:
                a, b, d = params
                self.memory[d] = a + b
            elif opcode == MULT:
                a, b, d = params
                self.memory[d] = a * b
            elif opcode == SAVE_TO:
                d = params[0]
                self.memory[d] = self.input
            elif opcode == OUTPUT:
                print(params[0])
            elif opcode == JUMP_IF_TRUE:
                a, b = params
                if a != 0:
                    self.pi = b
                    jumped = True
            elif opcode == JUMP_IF_FALSE:
                a, b = params
                if a == 0:
                    self.pi = b
                    jumped = True
            elif opcode == LESS_THAN:
                a, b, d = params
                self.memory[d] = 1 if a < b else 0
            elif opcode == EQUALS:
                a, b, d = params
                self.memory[d] = 1 if a == b else 0
            else:
                raise Exception("unknown opcode: {}".format(opcode))
            if not jumped:
                self.pi += len(params) + 1
