from file_utils import create_file


class TestFileCreator:

    def test_check_create_file_fail(self, mocker):

        filename = 'test_ip.txt'
        mocker.patch('builtins.open', side_effect=IOError)
        mock_logger = mocker.patch('file_utils.logger')

        result = create_file(filename)
        assert result is None

        mock_logger.exception.assert_called_once_with(
            f"An unexpected error occurred while creating a file:"
            f" {filename}"
        )

    def test_check_create_file_pass(self, mocker):

        filename = 'test_ip.txt'
        mock_logger = mocker.patch('file_utils.logger')
        assert create_file(filename)

        mock_logger.debug.assert_called_once_with(
            f"File '{filename}' has been created."
        )
