import os
import logging


CURRENT_IP_FILE = os.getenv('IP_FILE_NAME', 'current_ip.txt')
logger = logging.getLogger(__name__)


def check_api_input_value():
    API_BEARER_TOKEN = os.getenv('API_IP_TOKEN')
    if not API_BEARER_TOKEN:
        logger.error("API_BEARER_TOKEN is not set.")
        exit(1)
    return True


def check_frequency_input_value():
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


def check_log_level_input_value():
    VALID_LOG_LEVELS = {
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    }
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    if log_level not in VALID_LOG_LEVELS:
        logger.error(f"Invalid log level: '{log_level}'.")
        exit(1)
    return True


def check_input_values():
    check_api_input_value()
    check_frequency_input_value()
    check_log_level_input_value()
    return True
