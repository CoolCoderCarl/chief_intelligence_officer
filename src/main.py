import logging
import os
from platform import processor, uname
from time import sleep

from icmplib import ICMPLibError, multiping

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

logger = logging.getLogger()


try:
    IS_IPV6 = bool(os.getenv("IPV6"))
    if IS_IPV6:
        logger.info(f"IPv6 family set to {IS_IPV6}")
    VERBOSE = bool(os.getenv("VERBOSE"))
    if VERBOSE:
        logger.info(f"Verbose set to {VERBOSE}")
except KeyError as key_err:
    logging.warning(f"Key Error {key_err}")


def is_config_loaded() -> list:
    try:
        HOSTS = dynaconfig.settings["hosts"]
        return HOSTS
    except KeyError as key_err:
        logging.error(f"Err while loading config - {key_err}")
        return []


def multiping_requests(multihosts: list):
    """
    Show messages after requests using ICMP
    :param multihosts:
    :return:
    """
    try:
        for host in multihosts:
            if host.is_alive:
                if VERBOSE:
                    logging.info(host)
                else:
                    logging.info(
                        f"Host: {host.address} | Average RTT: {host.avg_rtt} | Jitter:  {host.jitter}"
                    )
            else:
                logging.warning(f"Host: {host.address} | Attempt successfully failed !")
    except ICMPLibError as icmp_err:
        logging.error(f"Error: {icmp_err}")


if __name__ == "__main__":
    while True:
        if IS_IPV6:
            multihosts = multiping(is_config_loaded(), family=6)
        else:
            multihosts = multiping(is_config_loaded())
        logger.info(f"Processor: {processor()}")
        sleep(1)
        logger.info(f"Uname: {uname()}")
        sleep(1)
        multiping_requests(multihosts)
        sleep(1)
