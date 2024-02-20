import logging
from logging.handlers import RotatingFileHandler

logger = None


def setup_logger():
    '''Logging.'''
    global logger
    if logger is None:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            'main.log', maxBytes=50000000, backupCount=5
        )
        logger.addHandler(handler)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
    return logger
