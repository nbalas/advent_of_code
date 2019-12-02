import logging
import hashlib
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__, logging.INFO)

# Part 1
MAGIC_HASH_PREFIX = "00000"
# Part 2
MAGIC_HASH_PREFIX_2 = "000000"


def main():

    secret_prefix = FileReader.read_input_as_string()
    current_postfix = 1
    while True:
        calculated_hash = calculate_md5(f"{secret_prefix}{current_postfix}")
        if validate_hash(calculated_hash):
            logging.info(f"Found hash {calculated_hash} with postfix: {current_postfix}")
            return
        current_postfix += 1


def calculate_md5(input_string):
    logging.debug(f"Calculating hash for input: {input_string}")
    return hashlib.md5(input_string.encode('utf-8')).hexdigest()


def validate_hash(hash_string):
    return hash_string.startswith(MAGIC_HASH_PREFIX_2)


if __name__ == "__main__":
    main()
