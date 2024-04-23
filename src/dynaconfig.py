import logging

from dynaconf import Dynaconf

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

settings = Dynaconf(
    settings_files=["/opt/settings.toml"],
)


if __name__ == "__main__":
    for data in settings:
        logging.info(f"Loaded variable {data}")
