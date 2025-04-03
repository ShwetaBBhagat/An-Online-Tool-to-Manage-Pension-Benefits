from flask import Blueprint, request, jsonify, url_for
from models.user_model import db, User
from models.pension_statement_model import db, PensionStatement
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
from flask import send_file
from utils.pdf_generator import StatementPDF
import io
from werkzeug.utils import secure_filename
from models.document_model import Document



auth_bp = Blueprint('auth_bp', __name__)  # Authentication Blueprint

UPLOAD_FOLDER = os.path.join(os.getcwd(), "backend", "uploads")
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@auth_bp.route('/user/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    profile_data = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "date_of_birth": current_user.date_of_birth,
        "ni_number": current_user.ni_number,
        "current_salary": float(current_user.current_salary) if current_user.current_salary else None,
        "employment_status": current_user.employment_status,
        "investment_type": current_user.investment_type,
        "address": current_user.address,
        "postal_code": current_user.postal_code,
        "contact_number": current_user.contact_number,
        "profile_completed": current_user.profile_completed
    }
    return jsonify(profile_data), 200


@auth_bp.route('/user/update-profile', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    data = request.get_json()

    current_user.date_of_birth = data.get("date_of_birth", current_user.date_of_birth)
    current_user.ni_number = data.get("ni_number", current_user.ni_number)
    current_user.current_salary = data.get("current_salary", current_user.current_salary)
    current_user.employment_status = data.get("employment_status", current_user.employment_status)
    current_user.investment_type = data.get("investment_type", current_user.investment_type)
    current_user.address = data.get("address", current_user.address)
    current_user.postal_code = data.get("postal_code", current_user.postal_code)
    current_user.contact_number = data.get("contact_number", current_user.contact_number)
    current_user.profile_completed = True

    db.session.commit()
    return jsonify({"message": "Profile updated successfully!"}), 200

@auth_bp.route('/user/statements', methods=['GET'])
@token_required
def get_user_statements(current_user):
    try:
        # Get all statements for the logged-in user
        statements = PensionStatement.query.filter_by(user_id=current_user.id).order_by(
            PensionStatement.statement_date.desc()
        ).all()

        result = []
        for s in statements:
            result.append({
                "statement_id": s.id,
                "statement_start_date": s.statement_start_date.strftime("%Y-%m-%d"),
                "statement_end_date": s.statement_end_date.strftime("%Y-%m-%d"),
                "statement_date": s.statement_date.strftime("%Y-%m-%d"),
                "account_number": s.account_number,
                "salary": str(s.salary),
                "employer_contribution": str(s.employer_contribution),
                "employee_contribution": str(s.employee_contribution),
                "total_contribution": str(s.total_contribution),
                "employer_percent": float(s.employer_percent),
                "employee_percent": float(s.employee_percent),
                "fund_name": s.fund_name,
                "fund_performance": str(s.fund_performance),
                "pot_value": str(s.pot_value)
            })

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@auth_bp.route('/user/statements/<int:statement_id>/download', methods=['GET'])
@token_required
def download_statement_pdf(current_user, statement_id):
    statement = PensionStatement.query.filter_by(id=statement_id, user_id=current_user.id).first()
    if not statement:
        return jsonify({"error": "Statement not found"}), 404

    # Prepare data
    data = {
        "Statement ID": statement.id,
        "Period": f"{statement.statement_start_date} to {statement.statement_end_date}",
        "Date Issued": statement.statement_date,
        "Pension Account": statement.account_number or "N/A",
        "Salary": f"£{statement.salary}",
        "Employer Contribution": f"£{statement.employer_contribution} ({statement.employer_percent}%)",
        "Employee Contribution": f"£{statement.employee_contribution} ({statement.employee_percent}%)",
        "Total Contribution": f"£{statement.total_contribution}",
        "Fund": statement.fund_name,
        "Fund Performance": f"{statement.fund_performance}%",
        "Pot Value": f"£{statement.pot_value}"
    }

    # Generate PDF
    pdf = StatementPDF()
    pdf.add_page()
    pdf.add_statement(data)

    # Output to BytesIO
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buffer = io.BytesIO(pdf_bytes)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"statement_{statement.id}.pdf",
        mimetype='application/pdf'
    )

@auth_bp.route('/user/upload-document', methods=['POST'])
@token_required
def upload_document(current_user):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        new_doc = Document(user_id=current_user.id, filename=filename, filepath=filepath)
        db.session.add(new_doc)
        db.session.commit()

        return jsonify({"message": "Document uploaded successfully!"}), 201

    return jsonify({"error": "File type not allowed"}), 400

@auth_bp.route('/user/documents', methods=['GET'])
@token_required
def list_user_documents(current_user):
    docs = Document.query.filter_by(user_id=current_user.id).all()
    result = [{"id": d.id, "filename": d.filename, "uploaded_at": d.uploaded_at.strftime("%Y-%m-%d %H:%M")} for d in docs]
    return jsonify({"documents": result}), 200

@auth_bp.route('/user/documents/<int:doc_id>/download', methods=['GET'])
@token_required
def download_document(current_user, doc_id):
    doc = Document.query.get(doc_id)
    if not doc:
        return jsonify({"error": "Document not found"}), 404

    # Role-based access: users can only access their own docs, admins can access all
    if current_user.id != doc.user_id and current_user.role != 'admin':
        return jsonify({"error": "Access denied"}), 403

    return send_file(doc.filepath, as_attachment=True, download_name=doc.filename)

@auth_bp.route('/user/analytics', methods=['GET'])
@token_required
def get_user_analytics(current_user):
    try:
        statements = PensionStatement.query.filter_by(user_id=current_user.id).order_by(
            PensionStatement.statement_date.asc()
        ).all()

        if not statements:
            return jsonify({"message": "No pension data found"}), 404

        # Build timeline data
        contributions_chart = []
        total_employee = 0
        total_employer = 0

        for s in statements:
            total_employee += float(s.employee_contribution)
            total_employer += float(s.employer_contribution)

            contributions_chart.append({
                "month": s.statement_date.strftime("%b %Y"),
                "employee_contribution": float(s.employee_contribution),
                "employer_contribution": float(s.employer_contribution),
                "pot_value": float(s.pot_value)
            })

        current_pot = float(statements[-1].pot_value)

        # Estimate growth rate (fallback to 5% if missing or unreliable)
        try:
            avg_growth = sum([float(s.fund_performance) for s in statements]) / len(statements)
        except:
            avg_growth = 5.0
        growth_rate = (avg_growth or 5.0) / 100

        # Project till UK retirement age (68)
        if current_user.date_of_birth:
            current_age = datetime.datetime.now().year - current_user.date_of_birth.year
            years_to_retire = max(0, 68 - current_age)
        else:
            years_to_retire = 30  # default

        projected_pot = round(current_pot * ((1 + growth_rate) ** years_to_retire), 2)

        return jsonify({
            "status": "success",
            "analytics": {
                "total_contributions": {
                    "employee": round(total_employee, 2),
                    "employer": round(total_employer, 2),
                    "combined": round(total_employee + total_employer, 2)
                },
                "average_growth_rate": round(growth_rate * 100, 2),
                "contributions_chart": contributions_chart,
                "projections": {
                    "current_pot": current_pot,
                    "years_to_retirement": years_to_retire,
                    "projected_pot_at_retirement": projected_pot
                }
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
