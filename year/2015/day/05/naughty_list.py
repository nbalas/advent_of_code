import logging
from logs.setup_logs import init_logs
from readers.file_reader import FileReader

logger = init_logs(__name__, logging.INFO)


def main():
    raw_list = FileReader.read_input_as_list()
    nice_list = list(filter(filter_repeated_letters,
                            filter(filter_vowel_requirement,
                                   filter(filter_bad_strings, raw_list))))
    logging.info(f"Santa's nice list has {len(nice_list)} entries")

    nice_list = list(filter(filter_in_between_repeat,
                                   filter(filter_two_letter_repeats, raw_list)))
    logging.info(f"Santa's NEW nice list has {len(nice_list)} entries")


###
# Part 1 Rules
###
# It does not contain the strings ab, cd, pq, or xy
def filter_bad_strings(input_string):
    naughty_strings = ['ab', 'cd', 'pq', 'xy']
    for naughty_string in naughty_strings:
        if naughty_string in input_string:
            return False
    return True


# Must contain three vowels: aeiou only
def filter_vowel_requirement(input_string):
    vowels = ['a', 'e', 'i', 'o', 'u']
    running_sum = 0
    for vowel in vowels:
        running_sum += input_string.count(vowel)
    return running_sum > 2


# Must have at least one letter that appears twice in a row
def filter_repeated_letters(input_string):
    previous_char = ''
    for character in input_string:
        if character == previous_char:
            return True
        previous_char = character
    return False


###
# Part 2 Rules
###
# It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy)
# or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
def filter_two_letter_repeats(input_string):
    for i in range(0, len(input_string)-1):
        if input_string.count(f"{input_string[i]}{input_string[i+1]}") > 1:
            return True
    return False


# It contains at least one letter which repeats with exactly one letter between them,
# like xyx, abcdefeghi (efe), or even aaa.
def filter_in_between_repeat(input_string):
    for i in range(0, len(input_string)-2):
        if input_string[i] == input_string[i+2]:
            return True
    return False


if __name__ == "__main__":
    main()
