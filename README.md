# public_ip_tracker
This program tracks the server's public IP address and sends a notification via Telegram if the IP changes. It periodically checks the IP, compares it with the previously stored one, and updates the record if needed. A Flask API endpoint (/current_ip) allows users to retrieve the current IP with proper authentication.
