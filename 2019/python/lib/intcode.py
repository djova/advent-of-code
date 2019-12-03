ADD = 1
MULT = 2
HALT = 99


def runcode(memory):
    mem = memory.copy()
    i = 0
    while (opcode := mem[i]) != HALT:
        if opcode == ADD:
            a, b, c = mem[i + 1:i + 4]
            mem[c] = mem[a] + mem[b]
            i += 4
        elif opcode == MULT:
            a, b, c = mem[i + 1:i + 4]
            mem[c] = mem[a] * mem[b]
            i += 4
        else:
            raise Exception("unknown opcode: {}".format(opcode))
    return mem
