from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__)


def main():
    list_input = FileReader.read_input_as_list()

    valid_passwords = 0

    for line in list_input:
        entry = line.split(':')
        condition = entry[0].split(' ')
        letter_range = list(map(int, condition[0].split('-')))
        required_letter = condition[1]
        password = entry[1].strip()

        if invalid_toboggan_policy(password, required_letter, letter_range):
            continue

        valid_passwords += 1

    logger.info("There are {} valid passwords".format(valid_passwords))


def invalid_sled_policy(password, required_letter, letter_range):
    password_letter_count = list(password).count(required_letter)
    return password_letter_count < letter_range[0] or password_letter_count > letter_range[1]


def invalid_toboggan_policy(password, required_letter, letter_range):
    char_password = list(password)
    both_places_filled = char_password[letter_range[0]-1] == required_letter and char_password[letter_range[1]-1] == required_letter
    neither_filled = char_password[letter_range[0]-1] != required_letter and char_password[letter_range[1]-1] != required_letter
    return both_places_filled or neither_filled


main()
