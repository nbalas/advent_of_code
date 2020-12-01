from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)

numbers = set(map(int, FileReader.read_input_as_list()))

end_product = 2020


def find_product(result):
    for num in numbers:
        other_pair = result-num
        if other_pair in numbers:
            logger.info("Found match! Numbers {} and {} will make a product of {}".format(num, other_pair, number*other_pair))
            return num, other_pair
    return None, None


for number in numbers:
    new_end_product = end_product - number
    second_piece, third_piece = find_product(new_end_product)
    if second_piece is None:
        continue
    logger.info("Found match! Numbers {} {} and {} will make a product of {}".format(number, second_piece, third_piece, number*second_piece*third_piece))
    break
