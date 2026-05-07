from file_utils import (
    write_current_ip,
    read_previous_ip,
    check_and_create_file
)
import pytest  # noqa: F401


class TestReadWriteCurrentIp:

    def test_successful_ip_write(self, tmp_path):
        filename = str(tmp_path / 'test_ip.txt')
        write_current_ip(filename, '192.168.1.1')
        with open(filename, 'r') as f:
            assert f.read() == '192.168.1.1'

    def test_write_exception(self, mocker):
        mocker.patch('builtins.open', side_effect=OSError)
        mock_logger = mocker.patch('file_utils.logger')

        write_current_ip('test_ip.txt', '192.168.1.1')

        mock_logger.exception.assert_called_once_with(
            "An error occurred while writing to test_ip.txt"
        )

    def test_read_existing_file(self, tmp_path):
        filename = tmp_path / 'test_ip.txt'
        filename.write_text('192.168.1.1')
        assert read_previous_ip(str(filename)) == '192.168.1.1'

    def test_read_non_existing(self, mocker):
        mocker.patch('builtins.open', side_effect=FileNotFoundError)
        mock_logger = mocker.patch('file_utils.logger')

        result = read_previous_ip('test_ip.txt')
        assert result is None

        mock_logger.error.assert_called_once_with(
            "File not found: test_ip.txt", exc_info=True
        )

    def test_read_exception(self, mocker):
        mocker.patch('builtins.open', side_effect=IOError)
        mock_logger = mocker.patch('file_utils.logger')

        result = read_previous_ip('test_ip.txt')
        assert result is None

        mock_logger.exception.assert_called_once_with(
            "An error occurred while reading test_ip.txt"
        )

    def test_check_file_not_exists(self, mocker):
        mock_logger = mocker.patch('file_utils.logger')
        mocker.patch('os.path.exists', return_value=False)
        check_and_create_file('current_ip.txt')
        mock_logger.debug.assert_called_once_with(
            "File 'current_ip.txt' has been created."
        )

    def test_check_file_exists(self, mocker):
        mock_logger = mocker.patch('file_utils.logger')
        mocker.patch('os.path.exists', return_value=True)
        check_and_create_file('current_ip.txt')
        mock_logger.debug.assert_called_once_with(
            "File 'current_ip.txt' already exists."
        )

    def test_check_file_not_exists_exception(self, mocker):
        mock_logger = mocker.patch('file_utils.logger')
        mocker.patch('os.path.exists', return_value=False)
        mocker.patch('builtins.open', side_effect=OSError)
        check_and_create_file('current_ip.txt')
        mock_logger.exception.assert_called_once_with(
            "An unexpected error occurred while creating a file:"
            " current_ip.txt"
        )
