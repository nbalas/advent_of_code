from logs.setup_logs import init_logs
from readers.file_reader import FileReader
from operator import methodcaller
from re import match
from queue import LifoQueue
from copy import copy

logger = init_logs(__name__)


def main():
    rules, messages = parse_input(FileReader.read_input_as_string())
    all_valid_messages = generate_all_messages(rules, [''])
    valid_messages = validate_messages(all_valid_messages, messages)
    logger.info(f"Total valid messages: {len(valid_messages)}")


def validate_messages(valid_messages, messages):
    return [msg for msg in messages if msg in valid_messages]


def generate_all_messages(rules, messages, idx='0'):
    options = rules[idx]
    all_messages = []
    for i, option in enumerate(options):
        # logger.debug(f"Looking for option {option} out of {options}")
        new_messages = copy(messages)
        for rule in option:
            if str.isdigit(rule):
                # logger.debug(f"Running method again for {rule}")
                new_messages = generate_all_messages(rules, new_messages, rule)
            elif rule:
                new_messages = [msg+rule for msg in new_messages]
        all_messages += new_messages
        # logger.debug(f"Messages {messages}, new messages {new_messages}")
    logger.debug(f"Returning back new messages: {all_messages}")
    return all_messages


def parse_input(raw_input):
    split_input = raw_input.split('\n\n')
    split_input[0] = split_input[0].replace('"', '')
    rules = list(map(methodcaller('split', ':'), split_input[0].split('\n')))
    rules = dict(map(lambda r: (r[0], list(map(lambda x: x.strip().split(' '), r[1].split('|')))), rules))
    messages = split_input[1].split('\n')
    return rules, messages


if __name__ == '__main__':
    main()