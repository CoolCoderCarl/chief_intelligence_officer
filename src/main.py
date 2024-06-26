import logging
import os
from platform import processor, uname
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

try:
    PLATFORM = bool(os.getenv("PLATFORM"))
    if PLATFORM:
        logger.info(f"Platform info activated !")
except KeyError as key_err:
    logging.warning(f"Key Error - {key_err}")

try:
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    if ENVIRONMENT:
        logger.info(f"Environment is set to {ENVIRONMENT} !")
except KeyError as key_err:
    logging.warning(f"Key Error - {key_err}")


def load_config(host_type: str) -> list:
    """
    Load settings.toml with dynaconf and return list of hosts
    If not return empty list
    :return:
    """
    try:
        if host_type == "icmp":
            HOSTS = dynaconfig.settings["ICMP"]["HOSTS"]
            return HOSTS
        if host_type == "http":
            HOSTS = dynaconfig.settings["HTTP"]["HOSTS"]
            return HOSTS
    except KeyError as key_err:
        logging.error(f"Err while loading config - Key Error - {key_err}")
        return []


def icmp_requests(hosts: list):
    """
    Show messages after requests using ICMP
    And then send an alert if configured
    :param hosts:
    :return:
    """
    try:
        for host in hosts:
            ping_result = ping(host)
            if ping_result.is_alive:
                if VERBOSE:
                    logging.info(
                        f"Host: {ping_result.address} | Average RTT: {ping_result.avg_rtt} ms | Jitter: {ping_result.jitter} ms"
                    )
                else:
                    logging.info(f"{host} is alive")
            else:  # TODO add map and send ip with associated resource name
                logging.error(
                    f"Host: {ping_result.address} | Attempt successfully failed !"
                )
                telegram_sender.send_alert_to_telegram(
                    f"Host: {ping_result.address} | Attempt successfully failed !",
                    environment=ENVIRONMENT,
                )
    except ICMPLibError as icmp_err:
        logging.error(f"ICMP Error - {icmp_err}")
        telegram_sender.send_alert_to_telegram(icmp_err, environment=ENVIRONMENT)


def http_requests(hosts: list):
    """
    Show messages after requests using HTTP
    And then send an alert if configured
    :param hosts:
    :return:
    """
    for host in hosts:
        try:
            logging.info(f"Going to request {host}")
            response = requests.get(
                f"http://{host}", timeout=dynaconfig.settings["REQUEST"]["TIMEOUT"]
            )
            if VERBOSE:
                logging.info(response.text)  # TODO parse json
                logging.info(response.headers)

            if response.status_code != 200:
                telegram_sender.send_alert_to_telegram(
                    f"Status code: {response.status_code} for this host: {host}",
                    environment=ENVIRONMENT,
                )
        except requests.exceptions.SSLError as ssl_err:
            logging.error(f"SSL Error - {ssl_err}")
            telegram_sender.send_alert_to_telegram(ssl_err, environment=ENVIRONMENT)
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout Error - {timeout_err}")
            telegram_sender.send_alert_to_telegram(timeout_err, environment=ENVIRONMENT)
        except requests.exceptions.ConnectionError as con_err:
            logging.error(f"Connection Error - {con_err}")
            telegram_sender.send_alert_to_telegram(con_err, environment=ENVIRONMENT)
        except requests.exceptions.BaseHTTPError as base_http_err:
            logging.error(f"Base HTTP Error - {base_http_err}")
            telegram_sender.send_alert_to_telegram(
                base_http_err, environment=ENVIRONMENT
            )


if __name__ == "__main__":
    icmp_hosts = load_config("icmp")
    http_hosts = load_config("http")
    while True:
        try:
            icmp_requests(icmp_hosts)
            http_requests(http_hosts)
            sleep(1)
            if PLATFORM:
                logger.info(f"Processor: {processor()}")
                sleep(1)
                logger.info(f"Uname: {uname()}")
                sleep(1)
        except ValueError as val_err:
            logging.warning(f"Config was not loaded - Value Error - {val_err}")
