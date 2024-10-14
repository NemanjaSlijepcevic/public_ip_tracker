from flask import Flask
import logging
import os
import threading
import time
from ip_checker import check_ip
from routes import setup_routes


frequency = int(os.getenv('CHECK_FREQUENCY', '60'))
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
VALID_LOG_LEVELS = {"NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


if log_level not in VALID_LOG_LEVELS:
    print(f"Invalid log level: '{log_level}'.")
    exit(1)

if not isinstance(frequency, int) and frequency <= 1:
    logger.error("Incorrect value of frequency")
    exit(1)


app = Flask(__name__)
setup_routes(app)


def periodic_task():
    def task():
        while True:
            try:
                check_ip()
            except Exception:
                logger.exception("Error occurred in periodic task")
            time.sleep(frequency)

    task_thread = threading.Thread(target=task)
    task_thread.daemon = True
    task_thread.start()


if __name__ == "__main__":
    logger.info("Starting public IP tracking app")
    periodic_task()
    app.run(host='0.0.0.0', port=5000)
