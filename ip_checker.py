import os
import logging
import requests
from dataclasses import dataclass, field
from datetime import datetime, timezone
from file_utils import read_previous_ip, write_current_ip


IP_SOURCES = [
    'http://ifconfig.me/ip',
    'https://api.ipify.org',
    'https://icanhazip.com',
]

CURRENT_IP_FILE = os.getenv('IP_FILE_NAME', 'current_ip.txt')

logger = logging.getLogger(__name__)


@dataclass
class IpState:
    current_ip: str = ''
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    last_checked: datetime = None
    last_changed: datetime = None


state = IpState()


def get_public_ip():
    for url in IP_SOURCES:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text.strip()
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error from {url}: {e}")
        except Exception:
            logger.warning(f"Failed to reach {url}", exc_info=True)
    logger.error("All IP sources failed")
    return None


def get_current_ip_value():
    if state.current_ip == '':
        cached = read_previous_ip(CURRENT_IP_FILE)
        if cached:
            state.current_ip = cached
        else:
            new_ip = get_public_ip()
            if new_ip:
                state.current_ip = new_ip
    return state.current_ip


def check_ip():
    new_ip = get_public_ip()
    state.last_checked = datetime.now(timezone.utc)
    previous_ip = read_previous_ip(CURRENT_IP_FILE)

    if new_ip is not None and new_ip != previous_ip:
        state.current_ip = new_ip
        state.last_changed = datetime.now(timezone.utc)
        logger.info(f"IP has changed from {previous_ip} to {new_ip}")
        write_current_ip(CURRENT_IP_FILE, new_ip)
    else:
        logger.debug("IP address is the same")
