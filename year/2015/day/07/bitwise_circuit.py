from readers.file_reader import FileReader


AND = "AND"
OR = "OR"
LSHIFT = "LSHIFT"
RSHIFT = "RSHIFT"
NOT = "NOT"
ASSIGN = "ASSIGN"

operations = {
    AND: lambda x: x[0] & x[1],
    OR: lambda x: x[0] | x[1],
    LSHIFT: lambda x: x[0] << x[1],
    RSHIFT: lambda x: x[0] >> x[1],
    NOT: lambda x: (2 ** 16) + ~x[0] if ~x[0] < 0 else ~x[0],
    ASSIGN: lambda x: x[0]
}


def get_operation(raw_op):
    params = raw_op.split(' ')
    if len(params) == 1:
        return ASSIGN, params[0]
    if len(params) == 2:
        return NOT, params[1]
    if len(params) == 3:
        return params[1], params[0], params[2]
    raise Exception(f"Unknown operation type: {raw_op}")


def parse_instruction(raw):
    return list(map(str.strip, raw.split("->")))


def flip_assigns(instruction):
    if is_int(instruction[0]):
        print(instruction)
    print(list(reversed(instruction)) if is_int(instruction[0]) else instruction)
    return list(reversed(instruction)) if is_int(instruction[0]) else instruction


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def resolve_wire_value(instruction, circuit, instructions):
    op = get_operation(instruction[0])
    op_vars = list(op[1:])
    current_wire = instruction[1]

    print(f"{op} -> {current_wire}")

    for i, var in enumerate(op_vars):
        if not is_int(var):
            if var not in circuit:
                op_vars[i] = resolve_wire_value(instructions[var], circuit, instructions)
            else:
                print(f"Resolving {var} to {circuit[var]}")
                op_vars[i] = int(circuit[var])
        else:
            op_vars[i] = int(op_vars[i])

    print(f"Operating on: {op_vars}")
    circuit[current_wire] = int(operations[op[0]](op_vars))
    print(f"Calculated: {circuit[current_wire]} for wire {current_wire}")
    return circuit[current_wire]


def main():
    find_wire = 'a'
    circuit = {}
    instructions = {i[1]: i for i in list(map(parse_instruction, FileReader.read_input_as_list()))}

    ## Part 2
    instructions['b'][0] = str(956)
    #########

    resolve_wire_value(instructions[find_wire], circuit, instructions)



    print(f"Wire a value: {circuit[find_wire]}")


if __name__ == '__main__':
    main()