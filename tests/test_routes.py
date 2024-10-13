from flask import Flask
from routes import setup_routes
import pytest  # noqa: F401

app = Flask(__name__)
setup_routes(app)
client = app.test_client()


class TestSetupRoutes:

    # Accessing /current_ip with valid Authorization header returns current IP
    def test_current_ip_with_valid_authorization(self, mocker):

        mocker.patch('routes.API_BEARER_TOKEN', 'valid_token')
        mocker.patch('routes.CURRENT_IP', '192.168.1.1')

        response = client.get(
            '/current_ip',
            headers={'Authorization': 'Bearer valid_token'}
        )

        assert response.status_code == 200
        assert response.json == {"ip": "192.168.1.1"}

    # Missing Authorization header results in 401 Unauthorized error
    def test_missing_authorization_header(self, mocker):

        response = client.get('/current_ip')

        assert response.status_code == 401
        assert response.json == {"error": "Unauthorized access"}
