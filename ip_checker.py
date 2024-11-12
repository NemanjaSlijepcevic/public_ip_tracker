import os
import logging
import requests
from file_utils import read_previous_ip, write_current_ip
from telegram_bot import send_telegram_message


CURRENT_IP_FILE = os.getenv('IP_FILE_NAME', 'current_ip.txt')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CURRENT_IP = ''

logger = logging.getLogger(__name__)


def get_public_ip():
    try:
        response = requests.get('http://ifconfig.me/ip')
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}", exc_info=True)
    except Exception:
        logger.exception(
            "An unexpected error occurred during GET request to ipconfig.me"
        )


def get_current_ip_value():
    if CURRENT_IP == '':
        new_ip = get_public_ip()
        set_current_ip_value(new_ip)
    return CURRENT_IP


def set_current_ip_value(current_value):
    global CURRENT_IP
    CURRENT_IP = current_value
    return True


def check_ip():
    new_ip = get_public_ip()
    previous_ip = read_previous_ip(CURRENT_IP_FILE)

    if new_ip != previous_ip and new_ip is not None:
        set_current_ip_value(new_ip)
        logger.info(f"IP has changed from {previous_ip} to {new_ip}")
        write_current_ip(CURRENT_IP_FILE, new_ip)
        message = f"Your IP address has changed to: {new_ip}"
        send_telegram_message(BOT_TOKEN, CHAT_ID, message)
    else:
        logger.debug("IP address is the same")
