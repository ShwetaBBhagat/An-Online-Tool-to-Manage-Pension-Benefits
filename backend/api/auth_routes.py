from flask import Blueprint, request, jsonify
from models.user_model import db, User
import pyotp
import re
from utils.email_service import send_welcome_email
from utils.helpers import generate_mfa_qr

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
