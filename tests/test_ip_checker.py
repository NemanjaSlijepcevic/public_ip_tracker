from ip_checker import get_public_ip, check_ip
import requests
import pytest  # noqa: F401


class TestGetCheckIp:

    # Successfully retrieves the public IP address from the external service
    def test_successful_ip_retrieval(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = '192.168.1.1\n'
        mocker.patch('requests.get', return_value=mock_response)

        ip = get_public_ip()

        assert ip == '192.168.1.1'

    # Handles HTTP errors gracefully and logs the error
    def test_http_error_handling(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("404 Client Error")
        )
        mocker.patch('requests.get', return_value=mock_response)
        mock_logger = mocker.patch('ip_checker.logger')

        ip = get_public_ip()

        assert ip is None
        mock_logger.error.assert_called_once_with(
            "HTTP error occurred: 404 Client Error", exc_info=True
        )

    def test_http_get_exception(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.ConnectionError("508 Error")
        )
        mocker.patch('requests.get', return_value=mock_response)
        mock_logger = mocker.patch('ip_checker.logger')

        ip = get_public_ip()

        assert ip is None
        mock_logger.exception.assert_called_once_with(
            "An unexpected error occurred during GET request to ipconfig.me"
        )

    def test_check_change_ip(self, mocker):
        mocker.patch('ip_checker.get_public_ip', return_value="192.168.1.100")
        mocker.patch('ip_checker.read_previous_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.write_current_ip')

        mocker.patch('ip_checker.send_telegram_message')
        mock_logger = mocker.patch('ip_checker.logger')

        check_ip()

        mock_logger.info.assert_called_once_with(
            "IP has changed from 192.168.1.1 to 192.168.1.100"
        )

    def test_check_unchanged_ip(self, mocker):

        mocker.patch('ip_checker.get_public_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.read_previous_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.write_current_ip')

        mocker.patch('ip_checker.send_telegram_message')
        mock_logger = mocker.patch('ip_checker.logger')

        check_ip()

        mock_logger.debug.assert_called_once_with("IP address is the same")
