# Public IP Tracker

Periodically polls your public IP address and exposes it over a secured REST API. Useful for machines behind Carrier-Grade NAT (CGNAT) where a static public IP is unavailable — run a VPN on the machine and query the API through it to always know the current IP.

IP changes are written to a file so the last known IP survives restarts. The app pairs with a separate log-reader service that handles notifications when the IP changes.

## API

### `GET /current_ip`

Returns the current public IP. Requires a bearer token.

```bash
curl -H "Authorization: Bearer your_api_token" http://localhost:5000/current_ip
```

```json
{ "ip": "123.45.67.89" }
```

### `GET /health`

Returns uptime and IP change timestamps. No authentication required.

```bash
curl http://localhost:5000/health
```

```json
{
  "status": "ok",
  "uptime_seconds": 3600,
  "last_checked": "2024-01-01T12:00:00+00:00",
  "last_changed": "2024-01-01T10:00:00+00:00"
}
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `API_IP_TOKEN` | Yes | — | Bearer token for `/current_ip` |
| `CHECK_FREQUENCY` | No | `60` | Seconds between IP checks (must be > 1) |
| `IP_FILE_NAME` | No | `current_ip.txt` | File used to persist the current IP |
| `LOG_LEVEL` | No | `INFO` | One of: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL |

## Running with Docker

The latest image is available at `ghcr.io/nemanjaslijepcevic/public_ip_tracker:latest`.

```bash
docker run -d \
  --name public_ip_tracker \
  -e API_IP_TOKEN="your_api_token" \
  -e TZ="Europe/Belgrade" \
  -v /path/to/current_ip.txt:/app/current_ip.txt:rw \
  --restart unless-stopped \
  ghcr.io/nemanjaslijepcevic/public_ip_tracker:latest
```

### Docker Compose

```yaml
services:
  public_ip_tracker:
    image: ghcr.io/nemanjaslijepcevic/public_ip_tracker:latest
    container_name: public_ip_tracker
    environment:
      API_IP_TOKEN: "${API_IP_TOKEN}"
      TZ: "Europe/Belgrade"
    volumes:
      - /path/to/current_ip.txt:/app/current_ip.txt:rw
    restart: unless-stopped
```

## Running Locally

```bash
pip install -r requirements.txt
API_IP_TOKEN=your_token python main.py
```

## Development

```bash
pip install -r requirements.txt
pip install pytest pytest-mock flake8

flake8 --statistics
pytest
```
