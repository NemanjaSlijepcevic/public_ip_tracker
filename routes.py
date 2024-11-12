import os
import logging
from ip_checker import get_current_ip_value
from flask import jsonify, request, abort

logger = logging.getLogger(__name__)
API_BEARER_TOKEN = os.getenv('API_IP_TOKEN')


def setup_routes(app):
    @app.route('/current_ip', methods=['GET'])
    def show_current_ip():
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.split(" ")[1] == API_BEARER_TOKEN:
            current_ip = get_current_ip_value()
            return jsonify({"ip": current_ip})
        else:
            abort(401)  # Unauthorized

    @app.errorhandler(401)
    def custom_401(error):
        return jsonify({"error": "Unauthorized access"}), 401
