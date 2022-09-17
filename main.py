import logging
import sys
from platform import processor, uname
from time import sleep

log_format = "%(levelname)s | %(asctime)s - %(message)s"

logging.basicConfig(
    stream=sys.stdout, filemode="w", format=log_format, level=logging.INFO
)

logger = logging.getLogger()

if __name__ == '__main__':
    while True:
        logger.info(f"Processor:  {processor()}")
        sleep(1)
        logger.info(f"Uname: {uname()}")
        sleep(1)
