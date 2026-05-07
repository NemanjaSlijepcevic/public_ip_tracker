import os
import pytest
from config_utils import check_api_token


class TestInputVariables:

    def test_check_api_token_failed(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "")

        with pytest.raises(SystemExit) as e:
            check_api_token()
        assert e.type == SystemExit
        assert e.value.code == 1

    def test_check_api_token_success(self, monkeypatch):
        monkeypatch.setenv("API_IP_TOKEN", "random_token")

        assert os.getenv("API_IP_TOKEN") == "random_token"
        assert check_api_token(), "check_api_token() exited unexpectedly"
