import os
import ip_checker
from datetime import datetime, timezone
from flask import jsonify, request, abort

API_BEARER_TOKEN = os.getenv('API_IP_TOKEN')


def setup_routes(app):
    @app.route('/current_ip', methods=['GET'])
    def show_current_ip():
        auth_header = request.headers.get('Authorization', '')
        parts = auth_header.split(' ', 1)
        token_ok = (
            len(parts) == 2
            and parts[0] == 'Bearer'
            and parts[1] == API_BEARER_TOKEN
        )
        if not token_ok:
            abort(401)
        return jsonify({"ip": ip_checker.get_current_ip_value()})

    @app.route('/health', methods=['GET'])
    def health():
        now = datetime.now(timezone.utc)
        s = ip_checker.state
        return jsonify({
            "status": "ok",
            "uptime_seconds": round((now - s.started_at).total_seconds()),
            "last_checked": s.last_checked.isoformat()
            if s.last_checked else None,
            "last_changed": s.last_changed.isoformat()
            if s.last_changed else None,
        })

    @app.errorhandler(401)
    def custom_401(error):
        return jsonify({"error": "Unauthorized access"}), 401
