import logging
import sys

from otsourcing.settings import APP_NAME

log_format = logging.Formatter(
    "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(log_format)
logger.addHandler(consoleHandler)
