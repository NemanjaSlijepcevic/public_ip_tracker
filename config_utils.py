import os
import logging
from ip_checker import check_bot_inputs
from routes import check_api_input
from file_utils import check_and_create_file


CURRENT_IP_FILE = os.getenv('IP_FILE_NAME', 'current_ip.txt')
logger = logging.getLogger(__name__)


def check_frequency():
    frequency = os.getenv('CHECK_FREQUENCY', '60')
    try:
        frequency = int(frequency)
    except ValueError:
        logger.error("Incorrect value of frequency.")
        exit(1)

    if frequency <= 1:
        logger.error("Incorrect value of frequency.")
        exit(1)

    return frequency


def check_log_level():
    VALID_LOG_LEVELS = {
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    }
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    if log_level not in VALID_LOG_LEVELS:
        logger.error(f"Invalid log level: '{log_level}'.")
        exit(1)
    return True


def check_inputs():
    check_bot_inputs()
    check_api_input()
    check_and_create_file(CURRENT_IP_FILE)
    check_frequency()
    check_log_level()
    return True
