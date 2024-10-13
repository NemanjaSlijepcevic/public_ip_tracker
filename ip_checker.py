import os
import logging
import requests
from file_utils import read_previous_ip, write_current_ip
from telegram_bot import send_telegram_message


BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CURRENT_IP_FILE = os.getenv('IP_FILE_NAME', 'current_ip.txt')
CURRENT_IP = ''

logger = logging.getLogger(__name__)


def get_public_ip():
    try:
        response = requests.get('http://ipconfig.me/ip')
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}", exc_info=True)
    except Exception:
        logger.exception(
            "An unexpected error occurred during GET request to ipconfig.me"
            )


def check_ip():
    global CURRENT_IP
    CURRENT_IP = get_public_ip()
    previous_ip = read_previous_ip(CURRENT_IP_FILE)

    if CURRENT_IP != previous_ip:
        logger.info(f"IP has changed from {previous_ip} to {CURRENT_IP}")
        write_current_ip(CURRENT_IP_FILE, CURRENT_IP)
        message = f"Your IP address has changed to: {CURRENT_IP}"
        send_telegram_message(BOT_TOKEN, CHAT_ID, message)
    else:
        logger.debug("IP address is the same")
