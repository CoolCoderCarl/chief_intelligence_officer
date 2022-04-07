import logging
import sys

Log_Format = "%(levelname)s | %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    filemode="w",
                    format=Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()

while True:
    logger.debug("Debugging")
