import math
import copy

ADD = 1
MULT = 2
SAVE_TO = 3
OUTPUT = 4
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8
RELATIVE_BASE_OFFSET = 9
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
    EQUALS: (2, 1),
    RELATIVE_BASE_OFFSET: (1, 0)
}

# parameter modes

# value = value at address
POSITION_MODE = 0

# plain value
IMMEDIATE_MODE = 1

RELATIVE_MODE = 2


def extract_param_modes(instruction, op_io):
    for exp in range(2, op_io + 2):
        yield math.floor(instruction % (10 ** (exp + 1)) / 10 ** exp)


class Intcode:
    def __init__(self, memory, inputs=None):
        if not inputs:
            inputs = []
        self.memory = memory.copy()
        self.extra_memory = {}
        self.pi = 0
        self.inputs = inputs
        self.relative_base = 0

    def mget(self, i):
        if i < len(self.memory):
            return self.memory[i]
        else:
            return self.extra_memory.get(i, 0)

    def add_input(self, v):
        self.inputs.insert(0, v)

    def mset(self, i, v):
        if i < len(self.memory):
            self.memory[i] = v
        else:
            self.extra_memory[i] = v

    def extract_params(self, modes, n_out):
        for i, mode in enumerate(modes):
            is_out_param = i >= (len(modes) - n_out)
            val = self.mget(self.pi + i + 1)
            if mode == POSITION_MODE:
                yield val if is_out_param else self.mget(val)
            elif mode == IMMEDIATE_MODE:
                if is_out_param:
                    raise Exception("out param can never be in immediate mode")
                yield val
            elif mode == RELATIVE_MODE:
                pos = self.relative_base + val
                yield pos if is_out_param else self.mget(pos)
            else:
                raise Exception("unknown mode: {}".format(mode))

    def parse_instruction(self, instruction):
        opcode = instruction % 100
        n_in, n_out = op_io[opcode]
        param_modes = list(extract_param_modes(instruction, n_in + n_out))
        return opcode, list(self.extract_params(param_modes, n_out))

    def run_safe(self):
        try:
            for x in self.run():
                yield x
        except IndexError:
            pass

    def run(self):
        while (instruction := self.mget(self.pi)) != HALT:
            opcode, params = self.parse_instruction(instruction)
            jumped = False
            if opcode == ADD:
                a, b, d = params
                self.mset(d, a + b)
            elif opcode == MULT:
                a, b, d = params
                self.mset(d, a * b)
            elif opcode == SAVE_TO:
                d = params[0]
                self.mset(d, self.inputs.pop())
            elif opcode == OUTPUT:
                yield params[0]
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
                self.mset(d, 1 if a < b else 0)
            elif opcode == EQUALS:
                a, b, d = params
                self.mset(d, 1 if a == b else 0)
            elif opcode == RELATIVE_BASE_OFFSET:
                a = params[0]
                self.relative_base += a
            else:
                raise Exception("unknown opcode: {}".format(opcode))
            if not jumped:
                self.pi += len(params) + 1

    def __copy__(self):
        ic = Intcode(
            copy.copy(self.memory)
        )
        ic.inputs = copy.copy(self.inputs)
        ic.extra_memory = copy.copy(self.extra_memory)
        ic.pop = copy.copy(self.extra_memory)
        ic.pi = self.pi
        ic.relative_base = self.relative_base
        return ic
