import logging


class MaxLevel(logging.Filter):
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno < self.max_level


def logger_init():
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s]:[%(levelname)s]:[%(filename)s]:[%(funcName)s] --- %(message)s",
        datefmt="%Y-%m-%d %H-%M-%S",
    )
    cmd_handler = logging.StreamHandler()
    cmd_handler.setFormatter(formatter)
    cmd_handler.setLevel(logging.INFO)

    logger.addHandler(cmd_handler)
    return logger
