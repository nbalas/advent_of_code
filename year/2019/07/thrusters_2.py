import operator
import queue
import copy
import itertools
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

HALT = 99
ADD = 1
MULT = 2
SAVE = 3 # Input value to provided register
OUTPUT = 4 # Output given value
JUMP_TRUE = 5 # Jump if true
JUMP_FALSE = 6 # Jump if false
LESS_THAN = 7 # Less than
EQUALS = 8 # equals

HALT_PROGRAM = -1
NEXT_AMP = -2

AMPS = ['A', 'B', 'C', 'D', 'E']


def main():
    int_register = list(map(int, FileReader.read_input_as_string().rstrip().split(',')))

    max_signal = -1
    test_sequence = range(5, 10)
    for phase_inputs in list(itertools.permutations(test_sequence)):
        amplifiers = {a: copy.deepcopy(int_register) for a in AMPS}
        for count, phase_input in enumerate(phase_inputs):
            phase_queue = queue.Queue()
            phase_queue.put(phase_input)
            amplifiers[AMPS[count]] = [amplifiers[AMPS[count]], phase_queue, 0, queue.Queue()]
        amplifiers['A'][3].put(0)
        run_program(amplifiers)
        output = amplifiers['A'][3].get()
        print(f"Output for combination [{phase_inputs}]: {output}")
        max_signal = max(max_signal, output)
    print(f"Largest output: {max_signal}")


def run_program(amplifiers):
    amp_position = 0
    while True:
        current_amp = AMPS[amp_position % len(AMPS)]
        next_amp_input = amplifiers[AMPS[(amp_position + 1) % len(AMPS)]][3]
        amplifier_state = amplifiers[current_amp]
        working_position = handle_opt_code(amplifier_state[2],
                                           amplifier_state[0], amplifier_state[1], amplifier_state[3], next_amp_input)
        if working_position == HALT_PROGRAM and current_amp == 'E':
            break
        elif working_position == HALT_PROGRAM or working_position == NEXT_AMP:
            amp_position += 1
            print(f"Now working in amp: {AMPS[amp_position % len(AMPS)]}")
        else:
            amplifier_state[2] = working_position


def resolve_value(reference, mode, register):
    reference_value = register[reference]
    if mode:
        return reference_value
    return register[reference_value]


def three_param_operate(operand, code_position, mode, register):
    """
    This method will modify the register with the requested operation
    :param operand: This is an operator function: https://docs.python.org/3/library/operator.html
    :param mode: array with the modes of the operands we have
    :param code_position: The position of the opt code we are processing in the register
    :param register: The array representing the register
    """
    result = operand(resolve_value(code_position + 1, mode[0], register),
                     resolve_value(code_position + 2, mode[1], register))
    register[register[code_position + 3]] = result


def parse_instruction(raw_instruction):
    """
    ABCDE
    (0)1002
        DE - two-digit opcode,      02 == opcode 2
         C - mode of 1st parameter,  0 == position mode
         B - mode of 2nd parameter,  1 == immediate mode
         A - mode of 3rd parameter,  0 == position mode, omitted due to being a leading zero
    :param raw_instruction: Assuming int value
    :return: op_code, param_1_mode, param_2_mode, param_3_mode,
    """
    instruction = list(f"{raw_instruction:05}")
    op_code = int(''.join(instruction[3:5]))
    mode_1 = int(instruction[2])
    mode_2 = int(instruction[1])
    mode_3 = int(instruction[0])
    return op_code, mode_1, mode_2, mode_3


def handle_opt_code(position, register, phase_inputs, current_amp_inputs, next_amp_inputs):
    instruction = parse_instruction(register[position])
    opt_code = instruction[0]
    modes = instruction[1:]
    if opt_code == HALT:
        print(f"HALTING Program")
        return HALT_PROGRAM
    elif opt_code == ADD:
        three_param_operate(operator.add, position, modes, register)
        return position + 4
    elif opt_code == MULT:
        three_param_operate(operator.mul, position, modes, register)
        return position + 4
    elif opt_code == SAVE:
        print(f"Queue values, phase: {list(phase_inputs.queue)} outputs: {list(current_amp_inputs.queue)}")
        if not phase_inputs.empty():
            new_input = phase_inputs.get()
        elif not current_amp_inputs.empty():
            new_input = current_amp_inputs.get()
        else:
            print(f"Unable to find any inputs- suspend and move to the next AMP")
            return NEXT_AMP

        print(f"Setting input {new_input} to register {register[position + 1]}")
        register[register[position + 1]] = new_input
        return position + 2
    elif opt_code == OUTPUT:
        output_value = resolve_value(position + 1, modes[0], register)
        print(f"Optcode output: {output_value}")
        next_amp_inputs.put(output_value)
        return position + 2
    elif opt_code == JUMP_TRUE:
        if resolve_value(position + 1, modes[0], register) != 0:
            return resolve_value(position + 2, modes[1], register)
        return position + 3
    elif opt_code == JUMP_FALSE:
        if resolve_value(position + 1, modes[0], register) == 0:
            return resolve_value(position + 2, modes[1], register)
        return position + 3
    elif opt_code == LESS_THAN:
        register[register[position + 3]] = 1 if resolve_value(position + 1, modes[0], register) < resolve_value(position + 2, modes[1], register) else 0
        return position + 4
    elif opt_code == EQUALS:
        register[register[position + 3]] = 1 if resolve_value(position + 1, modes[0], register) == resolve_value(position + 2, modes[1], register) else 0
        return position + 4
    raise Exception(f"Invalid code! {instruction[0]} at position {position}")


if __name__ == "__main__":
    main()
