from file_utils import write_current_ip


class TestWriteCurrentIP:

    def test_successful_ip_write(self):
        filename = 'test_ip.txt'
        ip = '192.168.1.1'
        write_current_ip(filename, ip)
        with open(filename, 'r') as file:
            content = file.read()
        assert content == ip

    def test_write_non_existing(self, mocker):

        filename = 'test_ip.txt'
        ip = '192.168.1.1'
        mocker.patch('builtins.open', side_effect=FileNotFoundError)
        mock_logger = mocker.patch('file_utils.logger')

        result = write_current_ip(filename, ip)
        assert result is None

        mock_logger.error.assert_called_once_with(
            f"File not found: {filename}", exc_info=True
        )

    def test_write_exception(self, mocker):

        filename = 'test_ip.txt'
        ip = '192.168.1.1'

        mocker.patch('builtins.open', side_effect=OSError)
        mock_logger = mocker.patch('file_utils.logger')

        result = write_current_ip(filename, ip)
        assert result is None

        mock_logger.exception.assert_called_once_with(
            f"An error occurred while writing to {filename}"
        )
