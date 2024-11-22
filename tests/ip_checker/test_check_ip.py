from ip_checker import check_ip


class TestGetCheckIp:

    def test_check_change_ip(self, mocker):
        mocker.patch('ip_checker.get_public_ip', return_value="192.168.1.100")
        mocker.patch('ip_checker.read_previous_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.write_current_ip')

        mock_logger = mocker.patch('ip_checker.logger')

        check_ip()

        mock_logger.info.assert_called_once_with(
            "IP has changed from 192.168.1.1 to 192.168.1.100"
        )

    def test_check_unchanged_ip(self, mocker):

        mocker.patch('ip_checker.get_public_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.read_previous_ip', return_value="192.168.1.1")
        mocker.patch('ip_checker.write_current_ip')

        mock_logger = mocker.patch('ip_checker.logger')

        check_ip()

        mock_logger.debug.assert_called_once_with("IP address is the same")
