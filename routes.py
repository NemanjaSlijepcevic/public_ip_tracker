import os
import logging
from flask import jsonify, request, abort

logger = logging.getLogger(__name__)
API_BEARER_TOKEN = os.getenv('API_IP_TOKEN')
CURRENT_IP = ''


def check_api_input():  # UT fails if this is checked without function
    API_BEARER_TOKEN = os.getenv('API_IP_TOKEN')
    if not API_BEARER_TOKEN:
        logger.error("API_BEARER_TOKEN is not set.")
        exit(1)
    return True  # unit testing check


def setup_routes(app):
    @app.route('/current_ip', methods=['GET'])
    def show_current_ip():
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.split(" ")[1] == API_BEARER_TOKEN:
            return jsonify({"ip": CURRENT_IP})
        else:
            abort(401)  # Unauthorized

    @app.errorhandler(401)
    def custom_401(error):
        return jsonify({"error": "Unauthorized access"}), 401
