import os
import pytest
from config_utils import (
    check_frequency,
    check_log_level,
    check_inputs
)


class TestInputVariables:

    def test_check_frequency_too_small(self, monkeypatch, mocker):
        monkeypatch.setenv("CHECK_FREQUENCY", "1")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("CHECK_FREQUENCY") == "1"

        with pytest.raises(SystemExit) as e:
            check_frequency()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of frequency."
        )

    def test_check_frequency_incorrect(self, monkeypatch, mocker):
        monkeypatch.setenv("CHECK_FREQUENCY", "error")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("CHECK_FREQUENCY") == "error"

        with pytest.raises(SystemExit) as e:
            check_frequency()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of frequency."
        )

    def test_check_frequency_success(self, monkeypatch):
        monkeypatch.setenv("CHECK_FREQUENCY", "50")

        assert check_frequency() == 50

    def test_check_log_level_error(self, monkeypatch, mocker):
        monkeypatch.setenv("LOG_LEVEL", "not_working")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("LOG_LEVEL") == "not_working"

        with pytest.raises(SystemExit) as e:
            check_log_level()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with(
            "Invalid log level: 'NOT_WORKING'."
        )

    def test_check_log_level_success(self, monkeypatch):
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        assert check_log_level()

    def test_check_inputs_success(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "random_api_token")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "random_chat_id")
        monkeypatch.setenv("CHECK_FREQUENCY", "50")
        monkeypatch.setenv("API_BEARER_TOKEN", "random_api_token")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        assert check_inputs()

    def test_check_inputs_failed(self, monkeypatch, mocker):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "random_api_token")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "random_chat_id")
        monkeypatch.setenv("CHECK_FREQUENCY", "five")
        monkeypatch.setenv("API_BEARER_TOKEN", "random_api_token")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        mock_logger = mocker.patch('config_utils.logger')

        with pytest.raises(SystemExit) as e:
            check_inputs()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of frequency."
        )
