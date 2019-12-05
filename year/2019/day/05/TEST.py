import logging
import operator
import copy
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

HALT = 99
ADD = 1
MULT = 2
SAVE = 3 # Input value to provided register
OUTPUT = 4 # Output given value


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


def handle_opt_code(position, register):
    instruction = parse_instruction(register[position])
    if instruction[0] == HALT:
        logging.info("Final value for position 0 is: %s", register[0])
        return -1
    elif instruction[0] == ADD:
        three_param_operate(operator.add, position, instruction[1:], register)
        return position + 4
    elif instruction[0] == MULT:
        three_param_operate(operator.mul, position, instruction[1:], register)
        return position + 4
    elif instruction[0] == SAVE:
        register[register[position + 1]] = input_value
        return position + 2
    elif instruction[0] == OUTPUT:
        print(f"Optcode output: {resolve_value(position + 1, instruction[1], register)}")
        return position + 2
    raise Exception(f"Invalid code! {instruction[0]}")


def run_program(register):
    working_position = 0
    while True:
        working_position = handle_opt_code(working_position, register)
        if working_position < 0:
            return register[0]


int_register = list(map(int, FileReader.read_input_as_string().rstrip().split(',')))

input_value = 1

run_program(int_register)
