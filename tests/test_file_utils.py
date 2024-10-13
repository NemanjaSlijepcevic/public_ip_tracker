from file_utils import write_current_ip, read_previous_ip
import pytest  # noqa: F401


class TestReadWriteCurrentIp:

    # Successfully writes a valid IP address to a file
    def test_successful_ip_write(self):
        filename = 'test_ip.txt'
        ip = '192.168.1.1'
        write_current_ip(filename, ip)
        with open(filename, 'r') as file:
            content = file.read()
        assert content == ip

    # Successfully reads and returns the content of an existing file
    def test_read_existing_file(self):
        filename = 'test_ip.txt'
        expected_content = '192.168.1.1'
        result = read_previous_ip(filename)
        assert result == expected_content

    # Handles a non-existent file by logging an error and returning None
    def test_handle_non_existent_file(self):
        filename = 'non_existent_file.txt'
        result = read_previous_ip(filename)
        assert result is None
