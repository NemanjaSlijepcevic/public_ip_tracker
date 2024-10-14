from telegram_bot import send_telegram_message
import requests
import pytest  # noqa: F401


class TestSendTelegramMessage:

    # Successfully sends a message with valid bot token and chat ID
    def test_successful_message_send(self, mocker):
        mock_post = mocker.patch('requests.post')
        mock_response = mocker.Mock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        bot_token = "valid_bot_token"
        chat_id = "valid_chat_id"
        message = "Hello, World!"

        response = send_telegram_message(bot_token, chat_id, message)

        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={'chat_id': chat_id, 'text': message}
        )
        assert response == mock_response

    # Handles invalid bot token gracefully
    def test_invalid_bot_token_handling(self, mocker):
        bot_token = "invalid_token"
        chat_id = "123456"
        message = "Hello, World!"
        mock_post = mocker.patch('requests.post')
        mock_response = mocker.Mock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("404 Client Error")
        )
        mock_post.return_value = mock_response
        mock_logger = mocker.patch('telegram_bot.logger')

        send_telegram_message(bot_token, chat_id, message)

        mock_logger.error.assert_called_once_with(
            "HTTP error occurred: 404 Client Error",
            exc_info=True
        )

    def test_invalid_post_request(self, mocker):
        bot_token = "valid_bot_token"
        chat_id = "valid_chat_id"
        message = "Hello, World!"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        # Mocking requests.post to raise an exception
        mock_post = mocker.patch('requests.post')
        mock_post.side_effect = Exception("Some unexpected error")

        # Mocking the logger to check if exception is logged
        mock_logger = mocker.patch('telegram_bot.logger')

        # Call the function
        send_telegram_message(bot_token, chat_id, message)

        # Assert that logger.exception was called with the right message
        mock_logger.exception.assert_called_once_with(
            f"An unexpected error occurred during POST request to {url}"
        )
