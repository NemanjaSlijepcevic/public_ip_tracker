import os
import logging

logger = logging.getLogger(__name__)


def read_previous_ip(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        logger.error(f"File not found: {filename}", exc_info=True)
        return None
    except Exception:
        logger.exception(f"An error occurred while reading {filename}")
        return None


def write_current_ip(filename, ip):
    try:
        with open(filename, 'w') as file:
            file.write(ip)
    except Exception:
        logger.exception(f"An error occurred while writing to {filename}")


def check_and_create_file(filename):
    if os.path.exists(filename):
        logger.debug(f"File '{filename}' already exists.")
    else:
        try:
            with open(filename, 'w'):
                logger.debug(f"File '{filename}' has been created.")
        except Exception:
            logger.exception(
                f"An unexpected error occurred while creating a file:"
                f" {filename}"
            )
