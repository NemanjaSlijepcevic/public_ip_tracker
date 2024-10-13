import os
from flask import jsonify, request, abort

API_BEARER_TOKEN = os.getenv('API_IP_TOKEN')
CURRENT_IP = ''


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
