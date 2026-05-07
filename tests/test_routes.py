import pytest
import ip_checker
from datetime import datetime, timezone
from flask import Flask
from ip_checker import IpState
from routes import setup_routes


@pytest.fixture
def client():
    app = Flask(__name__)
    setup_routes(app)
    return app.test_client()


class TestCurrentIpEndpoint:

    def test_valid_authorization(self, client, mocker):
        mocker.patch('routes.API_BEARER_TOKEN', 'valid_token')
        mocker.patch.object(
            ip_checker, 'state', IpState(current_ip='192.168.1.1')
        )

        response = client.get(
            '/current_ip',
            headers={'Authorization': 'Bearer valid_token'}
        )
        assert response.status_code == 200
        assert response.json == {"ip": "192.168.1.1"}

    def test_missing_authorization_header(self, client):
        response = client.get('/current_ip')
        assert response.status_code == 401
        assert response.json == {"error": "Unauthorized access"}

    def test_malformed_authorization_header(self, client):
        response = client.get(
            '/current_ip',
            headers={'Authorization': 'Bearertoken'}
        )
        assert response.status_code == 401
        assert response.json == {"error": "Unauthorized access"}


class TestHealthEndpoint:

    def test_health_returns_ok(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        data = response.json
        assert data['status'] == 'ok'
        assert 'uptime_seconds' in data
        assert 'last_checked' in data
        assert 'last_changed' in data
        assert 'current_ip' not in data

    def test_health_reflects_state(self, client, mocker):
        now = datetime.now(timezone.utc)
        mocker.patch.object(ip_checker, 'state', IpState(
            current_ip='1.2.3.4',
            last_checked=now,
            last_changed=now,
        ))

        response = client.get('/health')
        assert response.status_code == 200
        data = response.json
        assert data['last_checked'] is not None
        assert data['last_changed'] is not None
