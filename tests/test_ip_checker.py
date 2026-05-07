import ip_checker
from ip_checker import get_public_ip, check_ip, get_current_ip_value, IpState
import requests
import pytest  # noqa: F401


class TestGetPublicIp:

    def test_successful_ip_retrieval(self, mocker):
        mock_response = mocker.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = '192.168.1.1\n'
        mocker.patch('requests.get', return_value=mock_response)

        assert get_public_ip() == '192.168.1.1'

    def test_falls_back_to_second_source(self, mocker):
        success_response = mocker.Mock()
        success_response.raise_for_status.return_value = None
        success_response.text = '192.168.1.1\n'
        mocker.patch('requests.get', side_effect=[
            requests.exceptions.ConnectionError("first source down"),
            success_response,
        ])

        assert get_public_ip() == '192.168.1.1'

    def test_all_sources_fail(self, mocker):
        mocker.patch(
            'requests.get',
            side_effect=requests.exceptions.ConnectionError("down")
        )
        mock_logger = mocker.patch('ip_checker.logger')

        ip = get_public_ip()

        assert ip is None
        mock_logger.error.assert_called_once_with("All IP sources failed")


class TestCheckIp:

    def test_check_change_ip(self, mocker):
        fresh_state = IpState()
        mocker.patch.object(ip_checker, 'state', fresh_state)
        mocker.patch('ip_checker.get_public_ip', return_value="192.168.1.100")
        mocker.patch('ip_checker.read_previous_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.write_current_ip')
        mock_logger = mocker.patch('ip_checker.logger')

        check_ip()

        mock_logger.info.assert_called_once_with(
            "IP has changed from 192.168.1.1 to 192.168.1.100"
        )
        assert fresh_state.current_ip == "192.168.1.100"
        assert fresh_state.last_checked is not None
        assert fresh_state.last_changed is not None

    def test_check_unchanged_ip(self, mocker):
        fresh_state = IpState()
        mocker.patch.object(ip_checker, 'state', fresh_state)
        mocker.patch('ip_checker.get_public_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.read_previous_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.write_current_ip')
        mock_logger = mocker.patch('ip_checker.logger')

        check_ip()

        mock_logger.debug.assert_called_once_with("IP address is the same")
        assert fresh_state.last_checked is not None
        assert fresh_state.last_changed is None


class TestGetCurrentIpValue:

    def test_returns_cached_value(self, mocker):
        mocker.patch.object(
            ip_checker, 'state', IpState(current_ip='192.168.1.1')
        )
        assert get_current_ip_value() == '192.168.1.1'

    def test_reads_file_when_empty(self, mocker):
        mocker.patch.object(ip_checker, 'state', IpState())
        mocker.patch('ip_checker.read_previous_ip', return_value='192.168.1.1')
        assert get_current_ip_value() == '192.168.1.1'

    def test_falls_back_to_network(self, mocker):
        mocker.patch.object(ip_checker, 'state', IpState())
        mocker.patch('ip_checker.read_previous_ip', return_value=None)
        mocker.patch('ip_checker.get_public_ip', return_value='192.168.1.1')
        assert get_current_ip_value() == '192.168.1.1'

    def test_returns_empty_when_no_ip_available(self, mocker):
        mocker.patch.object(ip_checker, 'state', IpState())
        mocker.patch('ip_checker.read_previous_ip', return_value=None)
        mocker.patch('ip_checker.get_public_ip', return_value=None)
        assert get_current_ip_value() == ''
