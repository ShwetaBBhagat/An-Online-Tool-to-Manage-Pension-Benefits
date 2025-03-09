from flask import Blueprint, request, jsonify
from models.user_model import db, User
from flask_bcrypt import check_password_hash
import pyotp
import jwt
import datetime
from config import Config
import re
from utils.email_service import send_welcome_email
from utils.helpers import generate_mfa_qr
from utils.auth_middleware import token_required, admin_required

auth_bp = Blueprint('auth_bp', __name__)  # Authentication Blueprint


def is_strong_password(password):
    """
    Validates if a password is strong:
    - At least 8 characters long
    - Contains uppercase and lowercase letters
    - Contains at least one number
    - Contains at least one special character (@$!%*?&)
    """
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return "Password must include at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return "Password must include at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return "Password must include at least one number"
    if not re.search(r'[@$!%*?&]', password):
        return "Password must include at least one special character (@$!%*?&)"
    return None  # Password is strong

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        # Get user data from request
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # Default role is 'user'

        # Validate required fields
        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        # Validate email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format"}), 400

        # Validate password strength
        password_error = is_strong_password(password)
        if password_error:
            return jsonify({"error": password_error}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        # Generate MFA secret key
        mfa_secret = pyotp.random_base32()

        # Create new user
        new_user = User(
            name=name,
            email=email,
            role=role,
            mfa_secret=mfa_secret
        )
        new_user.set_password(password)  # Hash and store password

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        # Generate MFA QR Code
        qr_code_path = generate_mfa_qr(email, mfa_secret)

        # Send welcome email
        send_welcome_email(email, name)

        return jsonify({
            "message": "User registered successfully! A welcome email has been sent.",
            "mfa_secret": mfa_secret,
            "qr_code": qr_code_path
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Get user credentials from request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        mfa_token = data.get('mfa_token')  # MFA 6-digit OTP

        # Validate inputs
        if not email or not password or not mfa_token:
            return jsonify({"error": "Email, password, and MFA token are required"}), 400

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # Verify password
        if not check_password_hash(user.password, password):  # ✅ FIXED: Use Flask-Bcrypt
            return jsonify({"error": "Invalid email or password"}), 401

        # Verify MFA Token
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(mfa_token):
            return jsonify({"error": "Invalid MFA token"}), 401

        # Generate JWT token
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  # Token expires in 2 hours
        }
        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "access_token": token
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/admin/dashboard', methods=['GET'])
@token_required
@admin_required
def admin_dashboard(current_user):
    return jsonify({
        "message": "Welcome Admin!",
        "admin_id": current_user.id,
        "email": current_user.email
    }), 200
