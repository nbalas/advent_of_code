import logging

def init_logs(klass_name, level=logging.DEBUG):
    logging.basicConfig(level=level)
    return logging.getLogger(klass_name)