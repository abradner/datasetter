import logging
import sys
from os import environ


LOGGING_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

DEFAULT_LOGGING_LEVEL = 'info'
LOGGING_LEVEL = LOGGING_LEVELS[environ.get('LOGGING_LEVEL', DEFAULT_LOGGING_LEVEL)]


# Formatters
formatter = logging.Formatter(
    '%(levelname)s %(process)d %(thread)d %(asctime)s '
    '%(name)s.%(funcName)s:%(lineno)d - %(message)s'
)


# Handlers
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)


# Root level logger
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(LOGGING_LEVEL)


# Some third party libraries can spit out huge amounts of logs,
# we turn them off here.

libraries = [
    # 'snowflake',
]

for library in libraries:
    logging.getLogger(library).setLevel(logging.ERROR)
