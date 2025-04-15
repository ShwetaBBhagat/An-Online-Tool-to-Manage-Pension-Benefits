from flask import Blueprint, jsonify, request
from models import db
from models.user_model import User
from utils.auth_middleware import token_required, admin_required
from models.pension_statement_model import PensionStatement
from models.document_model import Document
from utils.email_service import send_statement_notification
from models.admin_model import Admin
from flask_bcrypt import check_password_hash
import jwt
import datetime
from config import Config
from utils.password_reset import generate_employer_token
from utils.email_service import send_employer_setup_email

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    admin = Admin.query.filter_by(email=email).first()
    if not admin or not check_password_hash(admin.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = jwt.encode({
        "admin_id": admin.id,
        "email": admin.email,
        "role": "admin",  # still include this to use in middleware
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, Config.JWT_SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Admin login successful",
        "access_token": token
    }), 200


# 🧑‍💼 Basic Admin Check Route
@admin_bp.route('/admin/ping', methods=['GET'])
@token_required
@admin_required
def admin_check(current_user):
    return jsonify({"message": f"Welcome, Admin {current_user.name}!"}), 200

#view registered users
@admin_bp.route('/admin/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(current_user):
    email = request.args.get('email')
    role = request.args.get('role')
    profile_completed = request.args.get('profile_completed')

    query = User.query

    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    
    if role:
        if role not in ['user', 'admin']:
            return jsonify({"error": "Invalid role. Must be 'user' or 'admin'"}), 400
        query = query.filter(User.role == role)

    if profile_completed:
        if profile_completed.lower() not in ['true', 'false']:
            return jsonify({"error": "profile_completed must be true or false"}), 400
        query = query.filter(User.profile_completed == (profile_completed.lower() == 'true'))

    users = query.order_by(User.created_at.desc()).all()

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role,
            "ni_number": u.ni_number,
            "profile_completed": u.profile_completed,
            "created_at": u.created_at.strftime('%Y-%m-%d %H:%M:%S') if u.created_at else None
        })

    return jsonify({
        "status": "success",
        "filters": {
            "email": email,
            "role": role,
            "profile_completed": profile_completed
        },
        "total_users": len(result),
        "users": result
    }), 200


#View Pension Statements for Any User
@admin_bp.route('/admin/user/<int:user_id>/statements', methods=['GET'])
@token_required
@admin_required
def get_user_statements_admin(current_user, user_id):
    from sqlalchemy import and_
    from models.pension_statement_model import PensionStatement

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Read query parameters
    start = request.args.get('start')
    end = request.args.get('end')
    min_salary = request.args.get('min_salary')
    max_salary = request.args.get('max_salary')
    fund_name = request.args.get('fund_name')
    min_perf = request.args.get('min_performance')
    max_perf = request.args.get('max_performance')

    # Build the query
    query = PensionStatement.query.filter_by(user_id=user_id)

    # Apply filters
    if start and end:
        try:
            start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
            query = query.filter(PensionStatement.statement_date.between(start_date, end_date))
        except ValueError:
            return jsonify({"error": "Invalid date format (use YYYY-MM-DD)"}), 400

    if min_salary:
        query = query.filter(PensionStatement.salary >= float(min_salary))
    if max_salary:
        query = query.filter(PensionStatement.salary <= float(max_salary))

    if fund_name:
        query = query.filter(PensionStatement.fund_name.ilike(f"%{fund_name}%"))

    if min_perf:
        query = query.filter(PensionStatement.fund_performance >= float(min_perf))
    if max_perf:
        query = query.filter(PensionStatement.fund_performance <= float(max_perf))

    statements = query.order_by(PensionStatement.statement_date.desc()).all()

    result = []
    for s in statements:
        result.append({
            "statement_id": s.id,
            "statement_date": s.statement_date.strftime("%Y-%m-%d"),
            "fund_name": s.fund_name,
            "salary": str(s.salary),
            "fund_performance": str(s.fund_performance),
            "total_contribution": str(s.total_contribution),
            "pot_value": str(s.pot_value)
        })

    return jsonify({
        "status": "success",
        "filters": {
            "start": start,
            "end": end,
            "min_salary": min_salary,
            "max_salary": max_salary,
            "fund_name": fund_name,
            "min_performance": min_perf,
            "max_performance": max_perf
        },
        "total_statements": len(result),
        "user_name": user.name,
        "statements": result
    }), 200


#Auto generate Pension Statement for Any User
@admin_bp.route('/admin/user/<int:user_id>/statements', methods=['POST'])
@token_required
@admin_required
def auto_generate_statement(current_user, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not user.current_salary or not user.investment_type:
        return jsonify({"error": "User salary and investment type are required"}), 400

    salary = float(user.current_salary)
    investment_type = user.investment_type

    # Use UK auto-enrolment rules
    if salary < 6240:
        return jsonify({"error": "Salary does not meet UK auto-enrolment threshold of £6,240"}), 400

    # Auto-calculate contributions
    employer_percent = 3.00
    employee_percent = 5.00
    employer_contribution = round(salary * (employer_percent / 100), 2)
    employee_contribution = round(salary * (employee_percent / 100), 2)
    total_contribution = round(employer_contribution + employee_contribution, 2)

    # Fund performance based on investment type
    performance_map = {
        "Low": 1.25,
        "Medium": 2.50,
        "High": 4.00
    }
    fund_performance = performance_map.get(investment_type, 2.0)
    fund_name = f"{investment_type} Risk Fund"

    # Pot value = last statement pot + new contribution (simulate)
    last_statement = PensionStatement.query.filter_by(user_id=user.id).order_by(
        PensionStatement.statement_date.desc()
    ).first()

    previous_pot = float(last_statement.pot_value) if last_statement else 0
    pot_value = round(previous_pot + total_contribution, 2)

    # Generate statement dates
    start_date = datetime.date.today().replace(day=1)
    end_date = (start_date + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

    new_statement = PensionStatement(
        user_id=user.id,
        statement_start_date=start_date,
        statement_end_date=end_date,
        statement_date=end_date,
        account_number=f"PB-{user.id:04d}",
        salary=salary,
        employer_contribution=employer_contribution,
        employee_contribution=employee_contribution,
        total_contribution=total_contribution,
        employer_percent=employer_percent,
        employee_percent=employee_percent,
        fund_name=fund_name,
        fund_performance=fund_performance,
        pot_value=pot_value
    )

    db.session.add(new_statement)
    send_statement_notification(user.email, user.name)
    db.session.commit()
    send_statement_notification(user.email, user.name)


    return jsonify({
        "message": "Pension statement auto-generated successfully",
        "user": user.email,
        "salary": salary,
        "investment_type": investment_type,
        "fund_performance": fund_performance,
        "pot_value": pot_value
    }), 201

#Delete Pension Statement
@admin_bp.route('/admin/statements/<int:statement_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_pension_statement(current_user, statement_id):
    from models.pension_statement_model import PensionStatement

    statement = PensionStatement.query.get(statement_id)
    if not statement:
        return jsonify({"error": "Pension statement not found"}), 404

    db.session.delete(statement)
    db.session.commit()

    return jsonify({
        "message": f"Pension statement ID {statement_id} has been deleted successfully."
    }), 200

#view documents
@admin_bp.route('/admin/documents', methods=['GET'])
@token_required
@admin_required
def view_all_documents(current_user):
    from sqlalchemy import and_, or_
    from models.document_model import Document

    # Get optional filters from query string
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    # Base query
    query = Document.query.join(User)

    # Apply filters
    if user_id:
        query = query.filter(Document.user_id == user_id)
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if start_date and end_date:
        try:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Document.uploaded_at.between(start, end))
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    documents = query.order_by(Document.uploaded_at.desc()).all()

    result = []
    for doc in documents:
        result.append({
            "document_id": doc.id,
            "filename": doc.filename,
            "uploaded_at": doc.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": doc.user.id,
            "user_name": doc.user.name,
            "user_email": doc.user.email
        })

    return jsonify({
        "status": "success",
        "filters": {
            "user_id": user_id,
            "email": email,
            "start": start_date,
            "end": end_date
        },
        "total_documents": len(result),
        "documents": result
    }), 200

#Admin Dashboard Summary Shows totals: users, employers, documents, statements, and pot value
@admin_bp.route('/admin/dashboard-summary', methods=['GET'])
@token_required
@admin_required
def admin_dashboard_summary(current_admin):
    from models.user_model import User
    from models.employer_model import Employer
    from models.pension_statement_model import PensionStatement
    from models.document_model import Document  # if your docs are stored here

    total_users = User.query.count()
    total_employers = Employer.query.count()
    total_documents = Document.query.count()
    total_statements = PensionStatement.query.count()

    pot_sum = db.session.query(
        db.func.sum(PensionStatement.pot_value)
    ).scalar() or 0.0

    return jsonify({
        "status": "success",
        "summary": {
            "total_users": total_users,
            "total_employers": total_employers,
            "total_documents": total_documents,
            "total_statements": total_statements,
            "total_pot_value": float(pot_sum)
        }
    }), 200


#View all employers
@admin_bp.route('/admin/employers', methods=['GET'])
@token_required
@admin_required
def get_all_employers(current_admin):
    from models.employer_model import Employer

    employers = Employer.query.order_by(Employer.created_at.desc()).all()
    result = []

    for e in employers:
        result.append({
            "id": e.id,
            "name": e.name,
            "email": e.email,
            "contact_number": e.contact_number,
            "address": e.address,
            "created_at": e.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({
        "status": "success",
        "total_employers": len(result),
        "employers": result
    }), 200

#Add Employer
@admin_bp.route('/admin/employers', methods=['POST'])
@token_required
@admin_required
def create_employer(current_admin):
    from models.employer_model import Employer
    from utils.password_reset import generate_employer_token
    from utils.email_service import send_employer_setup_email

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    contact_number = data.get("contact_number")
    address = data.get("address")

    if not all([name, email]):
        return jsonify({"error": "Name and email are required"}), 400

    if Employer.query.filter_by(email=email).first():
        return jsonify({"error": "Employer with this email already exists"}), 409

    # Step 1: Create employer (without password yet)
    new_employer = Employer(
        name=name,
        email=email,
        contact_number=contact_number,
        address=address
    )
    db.session.add(new_employer)
    db.session.commit()

    # Step 2: Generate token and setup link
    token = generate_employer_token(email)
    setup_link = f"https://yourfrontend.com/employer/set-password?token={token}"

    # Step 3: Send welcome/setup email
    send_employer_setup_email(email, name, setup_link)

    return jsonify({
        "message": "Employer created successfully. Setup email sent.",
        "email": email
    }), 201


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

#View Users of an Employer 
@admin_bp.route('/admin/employer/<int:employer_id>/users', methods=['GET'])
@token_required
@admin_required
def get_users_by_employer(current_admin, employer_id):
    from models.user_model import User

    users = User.query.filter_by(employer_id=employer_id).all()
    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "salary": float(user.current_salary or 0),
            "investment_type": user.investment_type,
            "ni_number": user.ni_number
        })

    return jsonify({
        "status": "success",
        "employer_id": employer_id,
        "total_users": len(result),
        "users": result
    }), 200

#Delete Employer
@admin_bp.route('/admin/employers/<int:employer_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_employer(current_admin, employer_id):
    from models.employer_model import Employer
    from models.user_model import User

    employer = Employer.query.get(employer_id)
    if not employer:
        return jsonify({"error": "Employer not found"}), 404

    users_exist = User.query.filter_by(employer_id=employer_id).first()
    if users_exist:
        return jsonify({"error": "Cannot delete employer with linked users"}), 400

    db.session.delete(employer)
    db.session.commit()

    return jsonify({"message": "Employer deleted successfully"}), 200

#