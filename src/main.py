import logging
import os
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

logger = logging.getLogger()

try:
    VERBOSE = bool(os.getenv("VERBOSE"))
    if VERBOSE:
        logger.info(f"Verbose set to {VERBOSE}")
except KeyError as key_err:
    logging.warning(f"Key Error - {key_err}")


def load_config() -> list:
    """
    Load settings.toml with dynaconf and return list of hosts
    If not return empty list
    :return:
    """
    try:
        HOSTS = dynaconfig.settings["hosts"]
        return HOSTS
    except KeyError as key_err:
        logging.error(f"Err while loading config - Key Error - {key_err}")
        return []


def ping_requests(hosts: list):
    """
    Show messages after requests using ICMP
    :param hosts:
    :return:
    """
    try:
        for host in hosts:
            host_result = ping(host)
            if host_result.is_alive:
                if VERBOSE:
                    logging.info(host_result)
                else:
                    logging.info(
                        f"Host: {host_result.address} | Average RTT: {host_result.avg_rtt} | Jitter: {host_result.jitter}"
                    )
            else:
                logging.warning(
                    f"Host: {host_result.address} | Attempt successfully failed !"
                )
    except ICMPLibError as icmp_err:
        logging.error(f"ICMP Error - {icmp_err}")


if __name__ == "__main__":
    hosts = load_config()
    while True:
        try:
            ping_requests(hosts)
            sleep(1)
        except ValueError as val_err:
            logging.warning(f"Config was not loaded - Value Error - {val_err}")
        logger.info(f"Processor: {processor()}")
        sleep(1)
        logger.info(f"Uname: {uname()}")
        sleep(1)
