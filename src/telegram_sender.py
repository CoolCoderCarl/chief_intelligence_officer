import email
import logging
import os

import requests

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
    ALERTING = bool(os.getenv("ALERTING"))
    if ALERTING:
        logger.info(f"Alerting activated !")
        try:
            API_TOKEN = dynaconfig.settings["TELEGRAM"]["API_TOKEN"]
            API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
            CHAT_ID = dynaconfig.settings["TELEGRAM"]["CHAT_ID"]
        except KeyError as key_err:
            logging.warning(f"Key Error - {key_err}")
except KeyError as key_err:
    logging.warning(f"Key Error - {key_err}")


def send_alert_to_telegram(message):
    """
    Send messages from mail to telegram
    :param message:
    :return:
    """
    # msg = email.message_from_bytes(message)
    try:
        response = requests.post(
            API_URL,
            json={
                "chat_id": CHAT_ID,
                "text": f"{message}",
            },
        )
        if response.status_code == 200:
            logging.info(
                f"Sent: {response.reason}. Status code: {response.status_code}"
            )
        else:
            logging.error(
                f"Not sent: {response.reason}. Status code: {response.status_code}"
            )
    except Exception as err:
        logging.error(err)


if __name__ == "__main__":
    pass
