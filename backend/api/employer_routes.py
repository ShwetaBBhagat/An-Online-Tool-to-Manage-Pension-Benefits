from flask import Blueprint, request, jsonify
from models.employer_model import Employer
from flask_bcrypt import check_password_hash
import jwt
import datetime
from config import Config
from utils.auth_middleware import token_required, employer_required, admin_required
from models import db



employer_bp = Blueprint('employer_bp', __name__)

#employer login
@employer_bp.route('/employer/login', methods=['POST'])
def employer_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    employer = Employer.query.filter_by(email=email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    if not check_password_hash(employer.password, password):
        return jsonify({"error": "Invalid password"}), 401

    token = jwt.encode({
        "employer_id": employer.id,
        "email": employer.email,
        "role": "employer",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, Config.JWT_SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Employer login successful",
        "access_token": token
    }), 200

#Employer View Their Users 
@employer_bp.route('/employer/my-users', methods=['GET'])
@token_required
@employer_required
def get_employer_users(current_user):
    from models.user_model import User
    from models.employer_model import Employer

    token = request.headers.get("Authorization").split(" ")[1]
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    employer_email = decoded.get('email')

    employer = Employer.query.filter_by(email=employer_email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    users = User.query.filter_by(employer_id=employer.id).all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "current_salary": float(user.current_salary or 0),
            "investment_type": user.investment_type,
            "ni_number": user.ni_number,
            "profile_completed": user.profile_completed
        })

    return jsonify({
        "status": "success",
        "total_users": len(result),
        "users": result
    }), 200

#view employer profile 
@employer_bp.route('/employer/profile', methods=['GET'])
@token_required
@employer_required
def get_employer_profile(current_user):
    from models.employer_model import Employer
    import jwt

    token = request.headers.get("Authorization").split(" ")[1]
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    email = decoded.get('email')

    employer = Employer.query.filter_by(email=email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    profile = {
        "id": employer.id,
        "name": employer.name,
        "email": employer.email,
        "contact_number": employer.contact_number,
        "address": employer.address,
        "created_at": employer.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }

    return jsonify({"status": "success", "profile": profile}), 200

#update employer profile
@employer_bp.route('/employer/update-profile', methods=['PUT'])
@token_required
@employer_required
def update_employer_profile(current_user):
    from models.employer_model import Employer
    import jwt

    token = request.headers.get("Authorization").split(" ")[1]
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    email = decoded.get('email')

    employer = Employer.query.filter_by(email=email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    data = request.get_json()
    employer.contact_number = data.get("contact_number", employer.contact_number)
    employer.address = data.get("address", employer.address)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200

#add user
@employer_bp.route('/employer/add-user', methods=['POST'])
@token_required
@employer_required
def add_user_by_employer(current_user):
    from models.user_model import User
    from models.employer_model import Employer
    from utils.email_service import send_welcome_email
    import bcrypt
    import pyotp
    import qrcode
    import os
    import datetime
    import jwt
    import re

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    salary = data.get("salary")
    date_of_birth = data.get("date_of_birth")
    investment_type = data.get("investment_type", "Medium")

    # Check required fields
    if not all([name, email, salary, date_of_birth]):
        return jsonify({"error": "All fields (name, email, salary, DOB) are required."}), 400

    # Validate email format
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email format."}), 400

    # Validate salary
    try:
        salary = float(salary)
        if salary < 0:
            return jsonify({"error": "Salary must be a positive number."}), 400
    except ValueError:
        return jsonify({"error": "Salary must be a number."}), 400

    # Validate DOB and legal age
    try:
        dob = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        age = (datetime.date.today() - dob).days // 365
        if age < 16:
            return jsonify({"error": "User must be at least 16 years old to be added."}), 400
        if age > 75:
            return jsonify({"error": "User exceeds the maximum pension eligibility age (75)."}), 400
    except ValueError:
        return jsonify({"error": "Invalid date of birth format. Use YYYY-MM-DD."}), 400

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "A user with this email already exists."}), 409

    # Get employer from token
    token = request.headers.get("Authorization").split(" ")[1]
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    employer_email = decoded.get('email')

    employer = Employer.query.filter_by(email=employer_email).first()
    if not employer:
        return jsonify({"error": "Employer not found."}), 404

    # auto-enrolment eligibility (UK NEST logic)
    auto_enrolled = (age >= 22 and salary >= 10000)

    # Generate MFA and temp password
    mfa_secret = pyotp.random_base32()
    otp_uri = f"otpauth://totp/PensionBenefits:{email}?secret={mfa_secret}&issuer=PensionBenefitsApp"

    qr_dir = os.path.join(os.getcwd(), "backend", "qrcodes")
    os.makedirs(qr_dir, exist_ok=True)

    qr_path = os.path.join(qr_dir, f"{email}_mfa.png")
    qrcode.make(otp_uri).save(qr_path)

    temp_password = bcrypt.hashpw("Welcome123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create and save user
    new_user = User(
        name=name,
        email=email,
        password=temp_password,
        date_of_birth=dob,
        current_salary=salary,
        investment_type=investment_type,
        mfa_secret=mfa_secret,
        employer_id=employer.id
    )

    db.session.add(new_user)
    db.session.commit()

    # Send welcome email with MFA QR
    send_welcome_email(email, name, qr_path)

    return jsonify({
        "message": "User added successfully via employer.",
        "auto_enrolled": auto_enrolled,
        "user_email": email
    }), 201

#view pension statements of their own employees
@employer_bp.route('/employer/user/<int:user_id>/statements', methods=['GET'])
@token_required
@employer_required
def get_user_statements_by_employer(current_user, user_id):
    from models.user_model import User
    from models.pension_statement_model import PensionStatement
    from models.employer_model import Employer
    import jwt

    # Decode employer info from token
    token = request.headers.get("Authorization").split(" ")[1]
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    employer_email = decoded.get("email")

    employer = Employer.query.filter_by(email=employer_email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    user = User.query.filter_by(id=user_id, employer_id=employer.id).first()
    if not user:
        return jsonify({"error": "User not found or does not belong to this employer."}), 403

    # Get user statements
    statements = PensionStatement.query.filter_by(user_id=user.id).order_by(PensionStatement.statement_date.desc()).all()

    result = []
    for s in statements:
        result.append({
            "statement_id": s.id,
            "statement_date": s.statement_date.strftime("%Y-%m-%d"),
            "statement_start_date": s.statement_start_date.strftime("%Y-%m-%d"),
            "statement_end_date": s.statement_end_date.strftime("%Y-%m-%d"),
            "salary": str(s.salary),
            "employee_percent": s.employee_percent,
            "employer_percent": s.employer_percent,
            "employee_contribution": str(s.employee_contribution),
            "employer_contribution": str(s.employer_contribution),
            "total_contribution": str(s.total_contribution),
            "fund_name": s.fund_name,
            "fund_performance": str(s.fund_performance),
            "pot_value": str(s.pot_value)
        })

    return jsonify({
        "status": "success",
        "user_id": user.id,
        "total_statements": len(result),
        "statements": result
    }), 200

#employer dashboard summary
@employer_bp.route('/employer/dashboard-summary', methods=['GET'])
@token_required
@employer_required
def employer_dashboard_summary(current_user):
    from models.user_model import User
    from models.pension_statement_model import PensionStatement
    from models.employer_model import Employer
    import jwt
    from sqlalchemy import func

    # Decode employer identity from token
    token = request.headers.get("Authorization").split(" ")[1]
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    employer_email = decoded.get("email")

    employer = Employer.query.filter_by(email=employer_email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    # Get all users under this employer
    users = User.query.filter_by(employer_id=employer.id).all()
    user_ids = [u.id for u in users]

    # Get total pot value
    total_pot = db.session.query(func.sum(PensionStatement.pot_value))\
        .filter(PensionStatement.user_id.in_(user_ids)).scalar() or 0

    total_users = len(users)
    avg_pot = round(total_pot / total_users, 2) if total_users > 0 else 0.00

    return jsonify({
        "status": "success",
        "summary": {
            "total_staff": total_users,
            "total_pot_value": float(total_pot),
            "average_pot_value": avg_pot
        }
    }), 200

#view uploaded documnets by their user
@employer_bp.route('/employer/documents', methods=['GET'])
@token_required
@employer_required
def get_employer_documents(current_user):
    from models.user_model import User
    from models.document_model import Document
    from models.employer_model import Employer
    import jwt

    # Decode employer email from token
    token = request.headers.get("Authorization").split(" ")[1]
    decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
    employer_email = decoded.get("email")

    employer = Employer.query.filter_by(email=employer_email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    # Get all user IDs under this employer
    users = User.query.filter_by(employer_id=employer.id).all()
    user_ids = [u.id for u in users]

    # Fetch documents linked to those users
    documents = Document.query.filter(Document.user_id.in_(user_ids)).order_by(Document.uploaded_at.desc()).all()

    result = []
    for doc in documents:
        result.append({
            "document_id": doc.id,
            "user_id": doc.user_id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "uploaded_at": doc.uploaded_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({
        "status": "success",
        "total_documents": len(result),
        "documents": result
    }), 200


#employer set password
@employer_bp.route('/employer/set-password', methods=['POST'])
def set_employer_password():
    from utils.password_reset import verify_employer_token
    from models.employer_model import Employer
    import bcrypt

    data = request.get_json()
    token = data.get("token")
    password = data.get("password")

    if not token or not password:
        return jsonify({"error": "Token and password required"}), 400

    email = verify_employer_token(token)
    if not email:
        return jsonify({"error": "Invalid or expired token"}), 400

    employer = Employer.query.filter_by(email=email).first()
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    employer.password = hashed_pw
    db.session.commit()

    return jsonify({"message": "Password has been set successfully!"}), 200
