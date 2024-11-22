# Public IP Tracking and Notification App

This application tracks your public IP address and provides a REST API endpoint to retrieve the current IP address, secured by a bearer token.

This setup is particularly useful for machines behind Carrier-Grade NAT (CGNAT), where direct access from the internet is not possible due to shared public IPs. By running a VPN on the machine, you can access the API endpoint securely via the VPN connection, even when the machine is behind CGNAT. This allows you to reliably track and retrieve the public IP address of your machine through the VPN without needing a public-facing IP address.

## Features

- **Public IP Tracking**: Periodically checks your public IP address.
- ~~**Telegram Notifications**: Sends a Telegram message when your IP changes.~~
- **REST API**: Provides an API to fetch the current IP address.
- **Logging**: Logs all actions to both the console and a log file (`app.log`).

## Prerequisites

- Python 3.12+
- A Telegram bot and a chat ID (set up using the Telegram Bot API).
- Docker (optional, for containerized deployment).
- Environment variables to configure the application.

## Setup

### Environment Variables

The application relies on the following environment variables:

| Variable                 | Description                                       |
|--------------------------|---------------------------------------------------|
| ~~`TELEGRAM_BOT_TOKEN`~~ | ~~Your Telegram bot token (required).~~               |
| ~~`TELEGRAM_CHAT_ID`~~   | ~~The chat ID where the bot sends notifications (required).~~ |
| `API_IP_TOKEN`           | Bearer token for accessing the `/current_ip` API (required). |
| `IP_FILE_NAME`           | Name of the file storing the current IP (default: `current_ip.txt`). |
| `LOG_LEVEL`              | Logging level (default: `INFO`). |
| `CHECK_FREQUENCY`        | Task execution frequency in sedonds (default: `60`). |


## Installation

1. Clone the repository:

   ~~~bash
   git clone https://github.com/nemanjaslijepcevic/public_ip_tracker.git
   cd public_ip_tracker
   ~~~

2. Install dependencies:

   ~~~bash
   pip install -r requirements.txt
   ~~~

3. Create a `.env` file with the required environment variables:

   ~~~env
   API_IP_TOKEN=your_api_token
   ~~~

4. Run the application:

   ~~~bash
   python main.py
   ~~~

The application will now start checking the public IP every minute and send a notification if it changes.

## API

### Get Current IP

You can retrieve the current public IP address by making a GET request to `/current_ip`:

- **URL**: `/current_ip`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <API_IP_TOKEN>`

Example:

~~~bash
curl -H "Authorization: Bearer your_api_token" http://localhost:5000/current_ip
~~~

Response:

~~~json
{
  "ip": "123.45.67.89"
}
~~~

## Docker

You can run the application in a Docker container using the provided `Dockerfile`. The latest Docker image for this application is available at **`ghcr.io/nemanjaslijepcevic/public_ip_tracker:latest`**.

### Using Pre-Built Docker Image

1. **Pull the latest image** from GitHub Container Registry (GHCR):

   ~~~bash
   docker pull ghcr.io/nemanjaslijepcevic/public_ip_tracker:latest
   ~~~

2. **Run the Docker container**:

   ~~~bash
   docker run -d \
     --name public_ip_tracker \
     -e API_IP_TOKEN="${API_IP_TOKEN}" \
     -e TZ="Europe/Belgrade" \
     -e LOG_LEVEL="DEBUG" \
     -v /path/to/public_ip_tracker/current_ip.txt:/app/current_ip.txt:rw \
     --restart unless-stopped \
     public_ip_tracker
   ~~~
   This command pulls and runs the container in detached mode (`-d`), mapping port `5000` on your host to port `5000` in the container. The `--env-file .env` flag ensures that the required environment variables are provided to the container.

### Docker Compose

For easier management of Docker containers and environment configuration, you can use **Docker Compose**.

1. Create a `docker-compose.yml` file in the root of your project:

   ~~~yaml
   version: '3'
   
   services:
     public_ip_tracker:
       image: ghcr.io/nemanjaslijepcevic/public_ip_tracker:latest
       container_name: public_ip_tracker
       environment:
         API_IP_TOKEN: "${API_IP_TOKEN}"
         TZ: "Europe/Belgrade"
         LOG_LEVEL: "DEBUG"
       volumes:
         - /path/to/current_ip.txt:/app/current_ip.txt:rw
       restart: unless-stopped
   ~~~

   This configuration does the following:
   - Builds the Docker image from the current directory.
   - Exposes the app on port `5000`.
   - Restarts the container unless it's stopped manually.

2. **Build and run with Docker Compose**:

   Run the following command to build and start the application using Docker Compose:

   ~~~bash
   docker-compose up --build -d
   ~~~

   The `--build` flag forces a rebuild of the Docker image, and `-d` runs the containers in detached mode.

3. **Stopping the app**:

   To stop the app when running with Docker Compose:

   ~~~bash
   docker-compose down
   ~~~

   This will stop and remove the containers but leave the images intact.

### Building and Running with Docker

1. **Build the Docker image**:

   ~~~bash
   docker build -t public_ip_tracker .
   ~~~

   This command will create a Docker image with the name `public_ip_tracker`.

2. **Run the Docker container**:

   Once the image is built, you can run the application in a Docker container:

   ~~~bash
   docker run -d -p 5000:5000 --env-file .env public_ip_tracker
   ~~~

   This will run the container in detached mode (`-d`), mapping port `5000` on your host to port `5000` in the container. The `--env-file .env` flag ensures that the required environment variables are provided to the container.

3. **Access the app**:

   After starting the container, the application will be accessible at `http://localhost:5000`.


This setup with Docker and Docker Compose makes it easy to deploy, manage, and run the application in a consistent environment.

## Running Tests

You can run the unit tests using `pytest`. If you have Docker configured for testing, you can use it as well.

1. **Run tests locally**:

   ~~~bash
   pytest
   ~~~

## Deployment

This application can be deployed on any server that supports Docker or directly with Python by running the application. Make sure to configure the environment variables correctly for the production environment.
