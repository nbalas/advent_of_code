from operator import methodcaller
from logs.setup_logs import init_logs
from readers.file_reader import FileReader
import re

logger = init_logs(__name__)

VALID_EYE_COLORS = ["amb", "blu", "brn", "gry", "grn",  "hzl",  "oth"]
REQUIRED_FIELDS = {
    "byr": lambda x: 1920 <= int(x) <= 2002,
    "iyr": lambda x: 2010 <= int(x) <= 2020,
    "eyr": lambda x: 2020 <= int(x) <= 2030,
    "hgt": lambda x: 150 <= int(x[:len(x)-2]) <= 193 if "cm" in x else 59 <= int(x[:len(x)-2]) <= 76 if re.search('in|cm', x) != None else False,
    "hcl": lambda x: re.search('^#[0-9a-f]{6}$', x) is not None,
    "ecl": lambda x: x in VALID_EYE_COLORS,
    "pid": lambda x: re.search('^[0-9]{9}$', x) is not None
}
OPTIONAL_FIELDS = ["cid"]


def main():
    passports = format_passports(FileReader.read_input_as_string())
    valid_passports = list(filter(validate_passport, passports))
    logger.info("There are {} valid passports.".format(len(valid_passports)))


def format_passports(raw_input):
    raw_passports = raw_input.split("\n\n")
    parsed_passports = list(map(lambda s: re.split(' |\n', s), raw_passports))
    formatted_passports = list(map(lambda p: dict(map(methodcaller('split', ':'), p)), parsed_passports))
    return formatted_passports


def validate_passport(passport):
    logger.debug("Processing passport {}".format(passport))
    for field in REQUIRED_FIELDS.keys():
        if field not in passport or not REQUIRED_FIELDS[field](passport[field]):
            logger.info("Passport is invalid! Missing or invalid required field {}".format(field))
            return False

    logger.info("Passport is valid!")
    return True


if __name__ == '__main__':
    main()