import jwt
from flask import request, jsonify
from config import Config
from functools import wraps
from models.user_model import User

def token_required(f):
    """Middleware to check if the user has a valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the token is provided in headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Extract Bearer token

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()

            if not current_user:
                return jsonify({"error": "User not found"}), 401

            return f(current_user, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

    return decorated

def admin_required(f):
    """Middleware to check if the user is an admin."""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403  # Forbidden
        return f(current_user, *args, **kwargs)

    return decorated
