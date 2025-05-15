from flask import Blueprint, request, jsonify, url_for
from flask_bcrypt import check_password_hash
from flask import send_file

from models.user_model import db, User
from models.pension_statement_model import db, PensionStatement
from models.document_model import Document
from models.beneficiary_model import Beneficiary

import bcrypt
import pyotp
import jwt
import datetime
from config import Config
import re
import os
import qrcode
import io
from werkzeug.utils import secure_filename

from utils.email_service import send_welcome_email, send_reset_email
from utils.password_reset import generate_reset_token, verify_reset_token
from utils.helpers import generate_mfa_qr
from utils.auth_middleware import token_required, admin_required
from utils.token_blacklist import blacklist_token
from utils.pdf_generator import StatementPDF

auth_bp = Blueprint('auth_bp', __name__)  # Authentication Blueprint

UPLOAD_FOLDER = os.path.join(os.getcwd(), "backend", "uploads")
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Employee Login
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
            "message": f"{user.role.capitalize()} login successful",
            "access_token": token,
            "role": user.role
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Employee Request Password reset
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

    # Generate reset token\
    reset_token = generate_reset_token(email)
    
    # Generate Reset Link
    reset_url = f"http://localhost:4200/reset-password?token={reset_token}"

    # Send email
    send_reset_email(email, reset_url)

    return jsonify({"message": "Password reset link sent to your email"}), 200

#Employee Password reset
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

#Employee Logout
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

#Employee Profile
@auth_bp.route('/user/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    return jsonify({
        "full_name": current_user.name,  # or current_user.full_name
        "email": current_user.email,
        "ni_number": current_user.ni_number,
        "date_of_birth": current_user.date_of_birth.isoformat() if current_user.date_of_birth else None,
        "current_salary": current_user.current_salary,
        "employment_status": current_user.employment_status,
        "investment_type": current_user.investment_type,
        "address": current_user.address,
        "postal_code": current_user.postal_code,
        "contact_number": current_user.contact_number,
        "employer_name": current_user.employer.name if current_user.employer else None
    }), 200


#Update Employee Profile
@auth_bp.route('/user/update-profile', methods=['PUT'])
@token_required
def update_user_profile(current_user):
    data = request.get_json()

    # === 1. Validate NI Number ===
    ni_number = data.get("ni_number")
    ni_regex = r'^[A-CEGHJ-PR-TW-Z]{2}\d{6}[A-D]$'
    if ni_number and not re.match(ni_regex, ni_number.upper()):
        return jsonify({"error": "Invalid UK NI number format (e.g., AB123456C)"}), 400

    # === 2. Validate DOB ===
    try:
        dob_str = data.get("date_of_birth")
        dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        if dob:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 16:
                return jsonify({"error": "You must be at least 16 years old"}), 400
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # === 3. Validate Salary ===
    salary = data.get("current_salary")
    if salary is not None and (not isinstance(salary, (int, float)) or salary < 6240):
        return jsonify({"error": "Salary must be at least £6,240 (UK qualifying threshold)"}), 400

    # === 4. Validate Postal Code ===
    postal_code = data.get("postal_code")
    postcode_regex = r"^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$"
    if postal_code and not re.match(postcode_regex, postal_code.upper()):
        return jsonify({"error": "Invalid UK postal code"}), 400

    # === 5. Validate Contact Number ===
    contact_number = data.get("contact_number")
    if contact_number and not re.match(r'^07\d{9}$', contact_number):
        return jsonify({"error": "Invalid UK mobile number. Format: 07XXXXXXXXX"}), 400

    # === 6. Validate Employment Status ===
    employment_status = data.get("employment_status")
    if employment_status and employment_status not in ["Active", "Retired"]:
        return jsonify({"error": "Invalid employment status. Choose 'Active' or 'Retired'"}), 400

    # === 7. Validate Investment Type ===
    investment_type = data.get("investment_type")
    if investment_type and investment_type not in ["Low", "Medium", "High"]:
        return jsonify({"error": "Invalid investment type. Choose 'Low', 'Medium', or 'High'"}), 400

    # ✅ Passed all validations, now update fields
    current_user.date_of_birth = dob or current_user.date_of_birth
    current_user.ni_number = ni_number or current_user.ni_number
    current_user.current_salary = salary or current_user.current_salary
    current_user.employment_status = employment_status or current_user.employment_status
    current_user.investment_type = investment_type or current_user.investment_type
    current_user.address = data.get("address", current_user.address)
    current_user.postal_code = postal_code or current_user.postal_code
    current_user.contact_number = contact_number or current_user.contact_number
    current_user.profile_completed = True

    db.session.commit()
    return jsonify({"message": "Profile updated successfully!"}), 200

#Employee Statements
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

#Employee Statements Download
@auth_bp.route('/user/statements/<int:statement_id>/download', methods=['GET'])
@token_required
def download_statement_pdf(current_user, statement_id):
    statement = PensionStatement.query.filter_by(id=statement_id, user_id=current_user.id).first()
    if not statement:
        return jsonify({"error": "Statement not found"}), 404

    # Prepare data
    data = {
        "Statement ID": statement.id,
        "Employee Name": statement.user.name,
        "Employer Name": statement.user.employer.name if statement.user and statement.user.employer else "N/A",
        "Period": f"{statement.statement_start_date.strftime('%d %b %Y')} to {statement.statement_end_date.strftime('%d %b %Y')}",
        "Date Issued": statement.statement_date.strftime('%d %b %Y'),
        "Pension Account": statement.account_number or "N/A",
        "Salary": f"£{float(statement.salary):,.2f}",
        "Employer Contribution": f"£{float(statement.employer_contribution):,.2f} ({statement.employer_percent}%)",
        "Employee Contribution": f"£{float(statement.employee_contribution):,.2f} ({statement.employee_percent}%)",
        "Total Contribution": f"£{float(statement.total_contribution):,.2f}",
        "Fund Name": statement.fund_name or "N/A",
        "Fund Performance": f"{float(statement.fund_performance):.2f}%",
        "Pot Value": f"£{float(statement.pot_value):,.2f}",
        "Risk Profile": statement.user.investment_type or "Not specified",
        "GDPR Notice": (
            "This statement contains sensitive personal and financial data. It is provided under UK GDPR "
            "for pension management purposes. Do not share or distribute. Contact dpo@yourcompany.com for any concerns."
        )
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

#Employee Document Upload
@auth_bp.route('/user/upload-document', methods=['POST'])
@token_required
def upload_document(current_user):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    document_type = request.form.get('document_type')  

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        new_doc = Document(
            user_id=current_user.id,
            filename=filename,
            filepath=filepath,
            document_type=document_type  
        )
        db.session.add(new_doc)
        db.session.commit()

        return jsonify({"message": "Document uploaded successfully!"}), 201

    return jsonify({"error": "File type not allowed"}), 400


#Employee Documents List
@auth_bp.route('/user/documents', methods=['GET'])
@token_required
def list_user_documents(current_user):
    docs = Document.query.filter_by(user_id=current_user.id).all()
    result = [{
        "id": d.id,
        "filename": d.filename,
        "uploaded_at": d.uploaded_at.strftime("%Y-%m-%d %H:%M"),
        "type": d.document_type or "Unknown"
    } for d in docs]
    return jsonify({"documents": result}), 200

#Employee View Documents
@auth_bp.route('/user/documents/<int:doc_id>/view', methods=['GET'])
def view_user_document(doc_id):
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is missing!"}), 401

    try:
        decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token.get('user_id')

        doc = Document.query.filter_by(id=doc_id, user_id=user_id).first()
        if not doc:
            return jsonify({"error": "Document not found"}), 404

        return send_file(doc.filepath, mimetype='application/pdf')

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

#Employee Document Download
@auth_bp.route('/user/documents/<int:doc_id>/download', methods=['GET'])
@token_required
def download_document(current_user, doc_id):
    doc = Document.query.get(doc_id)
    if not doc:
        return jsonify({"error": "Document not found"}), 404
    return send_file(doc.filepath, as_attachment=True, download_name=doc.filename)

#Employee Analytics
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
            employee_contribution = float(s.employee_contribution) if s.employee_contribution else 0.0
            employer_contribution = float(s.employer_contribution) if s.employer_contribution else 0.0
            pot_value = float(s.pot_value) if s.pot_value else 0.0

            total_employee += employee_contribution
            total_employer += employer_contribution

            contributions_chart.append({
                "month": s.statement_date.strftime("%b %Y"),
                "employee_contribution": employee_contribution,
                "employer_contribution": employer_contribution,
                "pot_value": pot_value
            })

        # Handle pot value for projections
        current_pot = contributions_chart[-1]["pot_value"]

        # Estimate growth rate (fallback to 5%)
        try:
            avg_growth = sum([float(s.fund_performance or 5.0) for s in statements]) / len(statements)
        except Exception:
            avg_growth = 5.0
        growth_rate = (avg_growth or 5.0) / 100

        # Project till UK retirement age (68)
        if current_user.date_of_birth:
            current_age = datetime.datetime.now().year - current_user.date_of_birth.year
            years_to_retire = max(0, 68 - current_age)
        else:
            years_to_retire = 30

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

#Employee Add Benificiary 
@auth_bp.route('/user/beneficiary', methods=['POST'])
@token_required
def add_or_update_beneficiary(current_user):
    data = request.get_json()

    full_name = data.get('full_name')
    relationship = data.get('relationship')
    percentage = data.get('percentage', 100)

    if not full_name:
        return jsonify({"error": "Full name is required"}), 400

    # Update if exists, else create new
    existing = Beneficiary.query.filter_by(user_id=current_user.id).first()

    if existing:
        existing.full_name = full_name
        existing.relationship = relationship
        existing.percentage = percentage
    else:
        new_b = Beneficiary(
            user_id=current_user.id,
            full_name=full_name,
            relationship=relationship,
            percentage=percentage
        )
        db.session.add(new_b)

    db.session.commit()
    return jsonify({"message": "Beneficiary saved successfully!"}), 200

#View Employee Benificiary
@auth_bp.route('/user/beneficiary', methods=['GET'])
@token_required
def get_beneficiary(current_user):
    beneficiary = Beneficiary.query.filter_by(user_id=current_user.id).first()

    if not beneficiary:
        return jsonify({"message": "No beneficiary found"}), 404

    return jsonify({
        "id": beneficiary.id,
        "full_name": beneficiary.full_name,
        "relationship": beneficiary.relationship,
        "percentage": float(beneficiary.percentage)
    }), 200