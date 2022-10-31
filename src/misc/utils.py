from loguru import logger


def log_debug(**kwargs):
    """
    Just a way for me to log variables quickly for debugging purposes.
    """
    for variable in kwargs.keys():
        logger.debug(f"\n{variable} : {kwargs[variable]}")



