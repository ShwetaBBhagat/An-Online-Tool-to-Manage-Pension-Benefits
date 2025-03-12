from flask import Blueprint, request, jsonify, url_for
from models.user_model import db, User
import bcrypt
from flask_bcrypt import check_password_hash
import pyotp
import jwt
import datetime
from config import Config
import re
from utils.email_service import send_welcome_email, send_reset_email
from utils.password_reset import generate_reset_token, verify_reset_token
from utils.helpers import generate_mfa_qr
from utils.auth_middleware import token_required, admin_required
import os
import qrcode
from utils.token_blacklist import blacklist_token

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
    """User Signup API with MFA, QR Code generation, and Welcome Email."""
    try:
        # Get user details from request
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # Default role: user

        # Validate inputs
        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

         # Validate email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format"}), 400

        # Ensure password is strong
        if len(password) < 8 or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) or not any(c in "!@#$%^&*()-_=+" for c in password):
            return jsonify({"error": "Password must be at least 8 characters long, include uppercase letters, numbers, and special symbols"}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Generate MFA Secret Key
        mfa_secret = pyotp.random_base32()

        # Generate MFA QR Code
        otp_uri = f"otpauth://totp/PensionBenefits:{email}?secret={mfa_secret}&issuer=PensionBenefitsApp"
        qr_code_dir = os.path.join(os.getcwd(), "backend", "qrcodes")

        # Ensure QR Code directory exists
        if not os.path.exists(qr_code_dir):
            os.makedirs(qr_code_dir)

        qr_code_path = os.path.join(qr_code_dir, f"{email}_mfa.png")
        qr = qrcode.make(otp_uri)
        qr.save(qr_code_path)

        # Save user to database
        new_user = User(name=name, email=email, password=hashed_password, role=role, mfa_secret=mfa_secret)
        db.session.add(new_user)
        db.session.commit()

        # Send welcome email with MFA QR Code
        send_welcome_email(email, name, qr_code_path)

        return jsonify({
            "message": "User registered successfully! A welcome email with your MFA QR Code has been sent.",
            "mfa_secret": mfa_secret,
            "qr_code": f"/qrcodes/{email}_mfa.png"
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

@auth_bp.route('/request-reset', methods=['POST'])
def request_reset():
    """Step 1: User requests a password reset."""
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Generate reset token
    reset_token = generate_reset_token(email)
    
    # Generate Reset Link
    reset_url = url_for('auth_bp.reset_password', token=reset_token, _external=True)

    # Send email
    send_reset_email(email, reset_url)

    return jsonify({"message": "Password reset link sent to your email"}), 200

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Step 2: User submits a new password with the reset token."""
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("password")

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    email = verify_reset_token(token)
    if not email:
        return jsonify({"error": "Invalid or expired token"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Hash new password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password has been reset successfully"}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Invalidate JWT token (Logout)"""
    token = None

    # Extract token from Authorization header
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]

    if not token:
        return jsonify({"error": "Token is missing!"}), 401

    try:
        # Decode token to check validity
        jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        
        # Blacklist token
        blacklist_token(token)

        return jsonify({"message": "Logged out successfully!"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has already expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401