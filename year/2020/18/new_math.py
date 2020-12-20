from logs.setup_logs import init_logs
from readers.file_reader import FileReader
from queue import LifoQueue
from copy import copy

logger = init_logs(__name__)

OPS = {
    '+': lambda v1, v2: v1 + v2,
    '*': lambda v1, v2: v1 * v2
}

INIT_VALUE = {
    '+': 0,
    '*': 1
}

OPEN_PAREN = '('
CLOSE_PAREN = ')'


def main():
    expressions = parse_input(FileReader.read_input_as_list())
    totals = [execute_expression(exp) for exp in expressions]
    logger.info(f"Final total is {sum(totals)}")


def parse_input(raw_input):
    return [list(map(lambda x: int(x) if str.isdigit(x) else x, exp.replace(' ', ''))) for exp in raw_input]


def execute_expression(exp):
    lifo = LifoQueue()
    total = 0

    for e in exp:
        if e is CLOSE_PAREN:
            single_exp = build_expression_list(lifo)
            lifo.put(process_single_expression_alt(single_exp))
        else:
            lifo.put(e)

    total += process_single_expression_alt(list(lifo.queue))
    return total


# Part 1
def process_single_expression(expression):
    logger.info(f"Processing expression {expression}")
    total = expression[0]
    op = None
    for value in expression[1:]:
        if value in OPS:
            op = value
        elif isinstance(value, int):
            if op:
                if total == 0:
                    total = INIT_VALUE[op]
                total = OPS[op](total, value)
                logger.info(f"New total {total}")
                op = None
        else:
            logger.error(f"Invalid expression {expression}")
    return total


# Part 2
def process_single_expression_alt(expression):
    logger.info(f"Processing alt expression {expression}")
    for priority in ['+', '*']:
        new_exp = []
        idx = 0
        while idx < len(expression):
            value = expression[idx]
            logger.info(f"{idx}, {value} and {expression}")
            logger.info(f"new exp: {new_exp}")
            if value is priority:
                result = OPS[value](expression[idx-1], expression[idx+1])
                expression = [result] + expression[idx+2:]
                idx = 0
                logger.info(f"Appending result {result}")
            elif value in OPS:
                new_exp.append(expression[idx-1])
                new_exp.append(value)
                idx += 1
                logger.info(f"Skipping op {value}")
            else:
                if len(expression) == 1 or idx == len(expression) - 1:
                    new_exp.append(expression[-1])
                    break
                logger.info(f"Not an op {value}")
                idx += 1
        logger.info(f"New expression for next iteration: {new_exp}")
        expression = copy(new_exp)

    return expression[0]


def build_expression_list(lifo):
    exp = []
    while not lifo.empty():
        item = lifo.get()
        if item is OPEN_PAREN:
            break
        exp.append(item)
    return list(reversed(exp))


if __name__ == '__main__':
    main()