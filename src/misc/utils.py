from loguru import logger
import sys


def log_debug(**kwargs):
    """
    Just a way for me to log variables quickly for debugging purposes.
    """
    for variable in kwargs.keys():
        logger.debug(f"\n{variable} : {kwargs[variable]}")


def check_running_from_venv():
    """
    Check if the Python interpreter is running from the venv. Taken from venv docs.
    """
    return sys.prefix == sys.base_prefix
