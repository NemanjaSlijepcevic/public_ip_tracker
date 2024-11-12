import pytest
from config_utils import check_chat_id_input_value


class TestChatIdInputValues:

    def test_check_chat_id_input_value_fail(self, monkeypatch, mocker):
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "")
        mock_logger = mocker.patch('config_utils.logger')
        with pytest.raises(SystemExit) as e:
            check_chat_id_input_value()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "CHAT_ID is not set."
        )

    def test_check_chat_id_input_value_pass(self, monkeypatch, mocker):
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "random_chat_id")

        result = check_chat_id_input_value()
        assert result, "check_chat_id_input_value() exited unexpectedly"
