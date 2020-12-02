import logging

class FileReader:

    DEFAULT_FILE_NAME = "input.txt"

    @staticmethod
    def read_input_as_list(filename=DEFAULT_FILE_NAME):
        """
        This method assumes we are reading from the working directory, will return a list of the file's lines
        :param filename: relative path to file
        """
        logging.info("Opening file %s", filename)
        with open(filename, 'r') as file:
            return set(map(str.strip, file.readlines()))

    @staticmethod
    def read_input_as_string(filename=DEFAULT_FILE_NAME):
        """
        This method assumes we are reading from the working directory, will return a string of the file
        :param filename: relative path to file
        """
        logging.info("Opening file %s", filename)
        with open(filename, 'r') as file:
            return file.read()
