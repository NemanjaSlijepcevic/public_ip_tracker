from file_utils import check_file_exists


class TestFileExistsChecker:

    def test_check_file_exists_fail(self, mocker):
        filename = 'test_ip_fail.txt'
        mocker.patch('os.path.exists', return_value=False)
        mocker.patch('builtins.open', side_effect=FileNotFoundError)
        result = check_file_exists(filename)
        assert result is None, "Checker should return False"

    def test_check_file_exists_pass(self, mocker):

        filename = 'test_ip.txt'
        mock_logger = mocker.patch('file_utils.logger')
        mocker.patch('os.path.exists', return_value=True)

        result = check_file_exists(filename)
        assert result, "Checker should return True"

        mock_logger.debug.assert_called_once_with(
            f"File '{filename}' already exists."
        )
