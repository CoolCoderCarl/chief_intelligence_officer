import logging
import sys
from platform import processor, uname
from time import sleep

log_format = "%(levelname)s | %(asctime)s - %(message)s"

logging.basicConfig(
    stream=sys.stdout, filemode="w", format=log_format, level=logging.DEBUG
)

logger = logging.getLogger()

while True:
    logger.debug("Debugging")
    sleep(1)
    logger.info("Processor: " + processor())
    sleep(1)
    logger.info("Uname: " + str(uname()))
    sleep(1)
