import logging
import sys

# Creating and Configuring Logger

Log_Format = "%(levelname)s | %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    filemode="w",
                    format=Log_Format,
                    level=logging.DEBUG)

logger = logging.getLogger()

# Testing our Logger
while True:
    # logger.info("Container is running now")
    logger.debug("Debug")
