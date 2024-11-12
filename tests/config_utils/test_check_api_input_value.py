import os
import pytest
from config_utils import check_api_input_value


class TestApiTokenInputVariables:

    def test_check_api_token_failed(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "")

        assert os.getenv("API_IP_TOKEN") == ""

        with pytest.raises(SystemExit) as e:
            check_api_input_value()
        assert e.type == SystemExit
        assert e.value.code == 1

    def test_check_api_token_success(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "random_token")

        result = check_api_input_value()
        assert result, "check_api_input_value() exited unexpectedly"
