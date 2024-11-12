import os
import pytest
from config_utils import check_frequency_input_value


class TestFrequencyInputVariables:

    def test_check_frequency_too_small(self, monkeypatch, mocker):
        monkeypatch.setenv("CHECK_FREQUENCY", "1")
        mock_logger = mocker.patch('config_utils.logger')

        assert os.getenv("CHECK_FREQUENCY") == "1"

        with pytest.raises(SystemExit) as e:
            check_frequency_input_value()
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
            check_frequency_input_value()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Incorrect value of frequency."
        )

    def test_check_frequency_success(self, monkeypatch):
        monkeypatch.setenv("CHECK_FREQUENCY", "50")

        result = check_frequency_input_value() == 50
        assert result, "check_frequency() exited unexpectedly"
