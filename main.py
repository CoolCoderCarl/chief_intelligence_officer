import logging
from platform import processor, uname
from time import sleep

from icmplib import ICMPLibError, ping

import dynaconfig

log_format = "%(levelname)s | %(asctime)s - %(message)s"

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.CRITICAL
)

logger = logging.getLogger()


def is_config_loaded():
    try:
        HOSTS = dynaconfig.settings["hosts"]
        return HOSTS
    except KeyError as key_err:
        logging.error(f"Err while loading config - {key_err}")
        return False


def icmp_requests(url: str):
    """
    Show messages after requests using ICMP
    :param url:
    :return:
    """
    try:
        host = ping(url, count=1, timeout=5)
        if host.is_alive:
            logging.info(
                f"Host: {url} | Is host available: {host.is_alive} - Average RTT: {host.avg_rtt}"
            )
        else:
            logging.warning(
                f"Host: {url} | Attempt successfully failed. | Is host available: {host.is_alive}"
            )
    except ICMPLibError as icmp_err:
        logging.error(f"Error: {icmp_err}")


if __name__ == "__main__":
    while True:
        logger.info(f"Processor: {processor()}")
        sleep(1)
        logger.info(f"Uname: {uname()}")
        sleep(1)
        if is_config_loaded():
            for host in is_config_loaded():
                icmp_requests(host)
                sleep(1)
