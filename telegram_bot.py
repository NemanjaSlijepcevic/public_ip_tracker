import logging
import requests

logger = logging.getLogger(__name__)


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}", exc_info=True)
    except Exception:
        logger.exception(
            f"An unexpected error occurred during POST request to {url}"
        )
