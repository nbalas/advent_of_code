from re import search
from collections import namedtuple
from operator import methodcaller
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)


def main():
    numbers = list(map(int, FileReader.read_input_as_string().split(',')))
    play_game(numbers, 30000000)


def play_game(numbers, max_index):
    numbers_called = {}

    # Initialize starting numbers
    for i, num in enumerate(numbers):
        if num not in numbers_called:
            numbers_called[num] = i

    starting_index = len(numbers) - 1
    for i in range(starting_index, max_index - 1):
        current_num = numbers[i]
        if current_num in numbers_called:
            next_num = i - numbers_called[current_num]
            numbers.append(next_num)
        else:
            numbers.append(0)
        numbers_called[current_num] = i
        # logger.info(f"Current num list {numbers_called}")
    logger.info(f"Final number list: {numbers}")
    logger.info(f"2002 number spoken was {numbers[-1]}")


if __name__ == '__main__':
    main()