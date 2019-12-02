import logging
import operator
import copy
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

HALT = 99
ADD = 1
MULT = 2


def operate(operand, code_position, register):
    """
    This method will modify the register with the requested operation
    :param operand: This is an operator function: https://docs.python.org/3/library/operator.html
    :param code_position: The position of the opt code we are processing in the register
    :param register: The array representing the register
    """
    result = operand(register[register[code_position+1]], register[register[code_position+2]])
    register[register[code_position+3]] = result


def handle_opt_code(position, register):
    code = register[position]
    if code == HALT:
        logging.info("Final value for position 0 is: %s", register[0])
        return -1
    elif code == ADD:
        operate(operator.add, position, register)
        return position + 4
    elif code == MULT:
        operate(operator.mul, position, register)
        return position + 4


def run_program(noun, verb, register):
    working_position = 0
    register[1] = noun
    register[2] = verb
    while True:
        working_position = handle_opt_code(working_position, register)
        if working_position < 0:
            return register[0]


int_register = list(map(int, FileReader.read_input_as_string().rstrip().split(',')))

compute_number = 19690720

# logging.info(run_program(12, 2, int_register))
#
# exit(0)

for noun_value in range(0, 99):
    for verb_value in range(0, 99):
        value = run_program(noun_value, verb_value, copy.deepcopy(int_register))
        logging.info("Ran program and got value: %s", value)
        if compute_number == value:
            logging.info("Successfully did math, noun: %s ; verb: %s ; answer: %s",
                         noun_value, verb_value, 100 * noun_value + verb_value)
            exit(0)




