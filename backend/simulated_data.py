from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

hashed_password = bcrypt.generate_password_hash("Welcome1!").decode('utf-8')
print(hashed_password)

# from app import app, db
# from models.pension_statement_model import PensionStatement
# from datetime import date, timedelta
# from decimal import Decimal

# def generate_statements_for_user(user_id, count=6):
#     today = date.today()
#     base_salary = Decimal('3000.00')
#     base_pot = Decimal('10000.00')
#     employer_percent = Decimal('3.00')
#     employee_percent = Decimal('5.00')

#     for i in range(count):
#         end_date = today.replace(day=1) - timedelta(days=30 * (count - i))
#         start_date = end_date - timedelta(days=30)

#         salary = base_salary + i * Decimal('50.00')
#         employer_contribution = round(salary * employer_percent / Decimal('100.00'), 2)
#         employee_contribution = round(salary * employee_percent / Decimal('100.00'), 2)
#         total_contribution = employer_contribution + employee_contribution
#         pot_value = base_pot + total_contribution * i + i * Decimal('250.00')
#         fund_performance = Decimal('1.50') + Decimal('0.25') * i

#         statement = PensionStatement(
#             user_id=user_id,
#             statement_start_date=start_date,
#             statement_end_date=end_date,
#             statement_date=end_date,
#             account_number=f"PS{user_id:03}-{i+1:02}",
#             salary=salary,
#             employer_contribution=employer_contribution,
#             employee_contribution=employee_contribution,
#             total_contribution=total_contribution,
#             employer_percent=employer_percent,
#             employee_percent=employee_percent,
#             fund_name="Balanced Growth Fund",
#             fund_performance=fund_performance,
#             pot_value=pot_value
#         )

#         db.session.add(statement)

#     db.session.commit()
#     print(f"{count} pension statements added for user {user_id}.")

# # Run inside Flask context
# with app.app_context():
#     generate_statements_for_user(user_id=1)
