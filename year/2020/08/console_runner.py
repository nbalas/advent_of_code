from collections import namedtuple
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

Operation = namedtuple("Operation", ("operation", "value"))

SWAP_OPS = {
    "jmp": "nop",
    "nop": "jmp"
}

OP_MOVEMENT = {
    "acc": lambda x: 1,
    "jmp": lambda x: x,
    "nop": lambda x: 1
}

REGISTER_MODIFIERS = {
    "acc": lambda register, value: register + value
}


def main():
    program = parse_program(FileReader.read_input_as_list())

    try:
        run_program(0, program, 0)
    except MemoryError:
        logger.info("Expected to fail for Part 1")

    run_program(0, program, 0, swap_ops=True)


def run_program(register, program, start_pointer, swap_ops=False):
    history = {}
    current_pointer = start_pointer
    while current_pointer < len(program):
        validate_infinite_loop(history, current_pointer, register)

        current_op = program[current_pointer].operation
        current_value = program[current_pointer].value

        if swap_ops and current_op in SWAP_OPS:
            logger.info(f"Attempting to swap {current_pointer} {current_op}")
            new_program = program.copy()
            new_program[current_pointer] = Operation(SWAP_OPS[current_op], current_value)
            try:
                run_program(0, new_program, 0)
                logger.info(f"Successfully ran program! Swapped {current_pointer} {current_op}")
                return
            except MemoryError:
                logger.info(f"Swapping pointer {current_pointer} op {current_op} failed")

        # Modify the register if needed
        if current_op in REGISTER_MODIFIERS:
            register = REGISTER_MODIFIERS[current_op](register, current_value)

        logger.info(f"Pointer {current_pointer} ran {current_op} {current_value}; Register is {register}")

        # Set pointer to the next operation
        current_pointer += OP_MOVEMENT[current_op](current_value)
    logger.info(f"Successfully ran program with Register {register}")


def validate_infinite_loop(history, current_pointer, register):
    if current_pointer in history:
        logger.info(f"Running pointer {current_pointer} again, we are in a infinite loop. Register state: {register}")
        raise MemoryError()
    history[current_pointer] = 1


def parse_program(raw_input):
    return list(map(lambda p: Operation(p[0], int(p[1])), map(lambda s: s.split(), raw_input)))


if __name__ == '__main__':
    main()