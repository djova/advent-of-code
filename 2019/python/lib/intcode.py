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


def runcode(memory, input=0):
    print("runcode-start")
    mem = memory.copy()
    i = 0

    def extract_params(param_modes, last_immediate=False):
        last_i = len(param_modes) - 1
        for p_i, mode in enumerate(param_modes):
            p_index = i + p_i + 1
            val = mem[p_index]
            if last_immediate and p_i == last_i:
                yield val
            elif mode == POSITION_MODE:
                yield mem[val]
            elif mode == IMMEDIATE_MODE:
                yield val
            else:
                raise Exception("unknown mode: {}".format(mode))

    while (instruction := mem[i]) != HALT:
        opcode, param_modes = parse_instruction(instruction)
        if opcode == ADD:
            a, b, result_i = list(extract_params(param_modes, True))
            mem[result_i] = a + b
            i += 4
        elif opcode == MULT:
            a, b, result_i = list(extract_params(param_modes, True))
            mem[result_i] = a * b
            i += 4
        elif opcode == SAVE_TO:
            result_i = mem[i + 1]
            mem[result_i] = input
            i += 2
        elif opcode == OUTPUT:
            params = list(extract_params(param_modes))
            print(params[0])
            i += 2
        elif opcode == JUMP_IF_TRUE:
            a, b = list(extract_params(param_modes))
            if a != 0:
                i = b
            else:
                i += 3
        elif opcode == JUMP_IF_FALSE:
            a, b = list(extract_params(param_modes))
            if a == 0:
                i = b
            else:
                i += 3
        elif opcode == LESS_THAN:
            a, b, result_i = list(extract_params(param_modes, True))
            mem[result_i] = 1 if a < b else 0
            i += 4
        elif opcode == EQUALS:
            a, b, result_i = list(extract_params(param_modes, True))
            mem[result_i] = 1 if a == b else 0
            i += 4
        else:
            raise Exception("unknown opcode: {}".format(opcode))
    print("runcode-done")
    return mem
