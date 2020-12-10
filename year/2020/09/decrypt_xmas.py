from collections import namedtuple
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)


PREAMBLE_SIZE = 25


def main():
    transmission = list(map(int, FileReader.read_input_as_list()))
    sums_to_check = transmission[PREAMBLE_SIZE:]
    invalid_sum = find_invalid_sum(transmission, sums_to_check)
    sumed_nums = find_numbers_to_sum_sum(transmission, invalid_sum)
    logger.info(f"Solution num is {min(sumed_nums) + max(sumed_nums)}")


# Part 1
def find_invalid_sum(transmission, sums_to_check):
    for count, num_sum in enumerate(sums_to_check):
        current_pointer = PREAMBLE_SIZE + count
        if not is_valid_sum(transmission[current_pointer - PREAMBLE_SIZE:current_pointer], transmission[current_pointer]):
            logger.info(f"Sum {num_sum} is not valid")
            return num_sum


def is_valid_sum(preamble, num_sum):
    preamble_set = set(preamble)
    for value in preamble_set:
        if num_sum - value in preamble_set:
            return True
    return False


# Part 2
def find_numbers_to_sum_sum(transmission, sum_to_sum):
    for count, num in enumerate(transmission):
        summing_nums = [num]
        running_sum = num
        for sum_num in transmission[count + 1:]:
            summing_nums.append(sum_num)
            running_sum += sum_num
            if sum_to_sum == running_sum:
                logger.info(f"Found our summing numbers! {summing_nums}")
                return summing_nums
            elif sum_to_sum < running_sum:
                break
    logger.info("Did not find any nums to sum to the sum we are summing for :(")


if __name__ == '__main__':
    main()