from ip_checker import get_current_ip_value


class TestGetCurrentIp:

    def test_get_current_ip_value(self, mocker):
        current_ip = "192.168.1.1"
        mocker.patch('ip_checker.CURRENT_IP', current_ip)
        assert current_ip == get_current_ip_value()

    def test_get_current_ip_value_empty(self, mocker):
        current_ip = "192.168.1.1"
        mocker.patch('ip_checker.CURRENT_IP', '')
        mocker.patch('ip_checker.get_public_ip', return_value="192.168.1.1")
        assert current_ip == get_current_ip_value()
