import logging
import os
from platform import processor, uname  # TODO add platform env var
from time import sleep

import requests
from icmplib import ICMPLibError, ping

import dynaconfig
import telegram_sender

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
        logger.info(f"Verbose activated !")
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


def icmp_requests(hosts: list):
    """
    Show messages after requests using ICMP
    :param hosts:
    :return:
    """
    try:
        for host in hosts:
            ping_result = ping(host)
            if ping_result.is_alive:
                if VERBOSE:
                    logging.info(
                        f"Host: {ping_result.address} TEST | Average RTT: {ping_result.avg_rtt} ms | Jitter: {ping_result.jitter} ms"
                    )
                else:
                    logging.info(f"{host} is alive")
            else:
                logging.warning(
                    f"Host: {ping_result.address} | Attempt successfully failed !"
                )
    except ICMPLibError as icmp_err:
        logging.error(f"ICMP Error - {icmp_err}")


def http_requests(hosts: list):
    """
    Show messages after requests using HTTP
    :param hosts:
    :return:
    """
    for h in hosts:
        try:
            logging.info(f"Going to request {h}")
            sleep(1)
            response = requests.get(f"http://{h}", timeout=10)
            logging.info(response.text)
            logging.info(response.headers)

            if response.status_code != 200:
                telegram_sender.send_alert_to_telegram(
                    f"Status code: {response.status_code} for this host: {h}"
                )
        except requests.exceptions.SSLError as ssl_err:
            logging.error(f"{ssl_err}")
            telegram_sender.send_alert_to_telegram(f"{ssl_err}")
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"{timeout_err}")
            telegram_sender.send_alert_to_telegram(f"{timeout_err}")
        except requests.exceptions.ConnectionError as con_err:
            logging.error(f"{con_err}")
            telegram_sender.send_alert_to_telegram(f"{con_err}")
        except requests.exceptions.BaseHTTPError as base_http_err:
            logging.error(f"{base_http_err}")
            telegram_sender.send_alert_to_telegram(f"{base_http_err}")


if __name__ == "__main__":
    hosts = load_config()
    while True:
        try:
            # icmp_requests(hosts)
            http_requests(hosts)
            sleep(1)
        except ValueError as val_err:
            logging.warning(f"Config was not loaded - Value Error - {val_err}")
        # logger.info(f"Processor: {processor()}")
        # sleep(1)
        # logger.info(f"Uname: {uname()}")
        # sleep(1)
