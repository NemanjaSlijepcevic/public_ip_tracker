import os
import pytest
from ip_checker import check_bot_inputs
from routes import check_api_input


class TestInputVariables:

    def test_check_bot_inputs_failed(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "")

        assert os.getenv("TELEGRAM_BOT_TOKEN") == ""
        assert os.getenv("TELEGRAM_CHAT_ID") == ""

        with pytest.raises(SystemExit) as e:
            check_bot_inputs()
        assert e.type == SystemExit
        assert e.value.code == 1

    def test_check_bot_inputs_success(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "random_bot_token")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "random_chat_id")

        assert os.getenv("TELEGRAM_BOT_TOKEN") == "random_bot_token"
        assert os.getenv("TELEGRAM_CHAT_ID") == "random_chat_id"

        try:
            check_bot_inputs()
        except SystemExit:
            pytest.fail(
                "check_bot_inputs() exited unexpectedly with SystemExit"
            )

    def test_check_api_token_failed(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "")

        assert os.getenv("API_IP_TOKEN") == ""

        with pytest.raises(SystemExit) as e:
            check_api_input()
        assert e.type == SystemExit
        assert e.value.code == 1

    def test_check_api_token_success(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "random_token")

        assert os.getenv("API_IP_TOKEN") == "random_token"

        try:
            check_api_input()
        except SystemExit:
            pytest.fail(
                "check_bot_inputs() exited unexpectedly with SystemExit"
            )
