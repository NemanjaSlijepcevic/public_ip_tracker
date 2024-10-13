# Public IP Tracking and Notification App

This application tracks your public IP address and notifies you via Telegram if the IP address changes. The app also provides a REST API endpoint to retrieve the current IP address, secured by a bearer token.

## Features

- **Public IP Tracking**: Periodically checks your public IP address.
- **Telegram Notifications**: Sends a Telegram message when your IP changes.
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

| Variable            | Description                                       |
|---------------------|---------------------------------------------------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (required).               |
| `TELEGRAM_CHAT_ID`   | The chat ID where the bot sends notifications (required). |
| `API_IP_TOKEN`       | Bearer token for accessing the `/current_ip` API (required). |
| `IP_FILE_NAME`       | Name of the file storing the current IP (default: `current_ip.txt`). |
| `LOG_LEVEL`          | Logging level (default: `INFO`). |
| `CHECK_FREQUENCY`    | Task execution frequency in sedonds (default: `60`). |


## Installation

1. Clone the repository:

   ~~~bash
   git clone https://github.com/yourusername/public_ip_tracker.git
   cd public_ip_tracker
   ~~~

2. Install dependencies:

   ~~~bash
   pip install -r requirements.txt
   ~~~

3. Create a `.env` file with the required environment variables:

   ~~~env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
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

You can run the application in a Docker container using the provided `Dockerfile`. Follow these steps to build and run the application.

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

### Docker Compose

For easier management of Docker containers and environment configuration, you can use **Docker Compose**.

1. Create a `docker-compose.yml` file in the root of your project:

   ~~~yaml
   version: '3'

   services:
     app:
       image: public_ip_tracker
       build: .
       ports:
         - "5000:5000"
       env_file:
         - .env
       restart: unless-stopped
   ~~~

   This configuration does the following:
   - Builds the Docker image from the current directory.
   - Exposes the app on port `5000`.
   - Loads environment variables from the `.env` file.
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

### Using Docker Compose for Development

During development, you may want to make changes to your code and rebuild the container. Docker Compose simplifies this process:

1. After making changes, rebuild the container:

   ~~~bash
   docker-compose up --build -d
   ~~~

   Docker Compose will automatically rebuild the image and restart the container.

2. To view logs from the running container:

   ~~~bash
   docker-compose logs -f
   ~~~

This setup with Docker and Docker Compose makes it easy to deploy, manage, and run the application in a consistent environment.

## Running Tests

You can run the unit tests using `pytest`. If you have Docker configured for testing, you can use it as well.

1. **Run tests locally**:

   ~~~bash
   pytest
   ~~~

## Deployment

This application can be deployed on any server that supports Docker or directly with Python by running the application. Make sure to configure the environment variables correctly for the production environment.
