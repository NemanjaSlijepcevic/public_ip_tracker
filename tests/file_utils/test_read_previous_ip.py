from file_utils import read_previous_ip


class TestReadCurrentIP:

    def test_read_existing_file(self, mocker):
        filename = 'test_ip.txt'
        mock_file = mocker.mock_open(read_data='192.168.1.1')
        mocker.patch('builtins.open', mock_file)

        result = read_previous_ip(filename)
        assert result == '192.168.1.1'

    def test_read_non_existing(self, mocker):

        filename = 'test_ip.txt'
        mocker.patch('builtins.open', side_effect=FileNotFoundError)
        mock_logger = mocker.patch('file_utils.logger')

        result = read_previous_ip(filename)
        assert result is None

        mock_logger.error.assert_called_once_with(
            f"File not found: {filename}", exc_info=True
        )

    def test_read_exception(self, mocker):

        filename = 'test_ip.txt'

        mocker.patch('builtins.open', side_effect=IOError)
        mock_logger = mocker.patch('file_utils.logger')

        result = read_previous_ip(filename)
        assert result is None

        mock_logger.exception.assert_called_once_with(
            f"An error occurred while reading {filename}"
        )
