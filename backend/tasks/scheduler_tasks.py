from models import db
from models.user_model import User
from models.pension_statement_model import PensionStatement
import datetime
from sqlalchemy import func

def generate_monthly_statements():
    print("Running Monthly Pension Statement Auto-Generator...")

    today = datetime.date.today()
    first_day = today.replace(day=1)
    last_day = (first_day + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)

    users = User.query.all()

    for user in users:
        if not user.current_salary or not user.date_of_birth:
            continue

        salary = float(user.current_salary)
        employee_percent = 5.0
        employer_percent = 3.0
        employee_contribution = round(salary * (employee_percent / 100), 2)
        employer_contribution = round(salary * (employer_percent / 100), 2)
        total_contribution = employee_contribution + employer_contribution

        # Simulate fund growth by investment type
        performance_map = {"Low": 2.5, "Medium": 5.0, "High": 8.0}
        growth_rate = performance_map.get(user.investment_type or "Medium", 5.0)

        last_pot = db.session.query(func.max(PensionStatement.pot_value)).filter_by(user_id=user.id).scalar() or 0.0
        new_pot = round(last_pot + total_contribution + (last_pot * (growth_rate / 100) / 12), 2)

        statement = PensionStatement(
            user_id=user.id,
            account_number=f"ACCT{user.id:05}",
            statement_date=today,
            statement_start_date=first_day,
            statement_end_date=last_day,
            salary=salary,
            employee_percent=employee_percent,
            employer_percent=employer_percent,
            employee_contribution=employee_contribution,
            employer_contribution=employer_contribution,
            total_contribution=total_contribution,
            fund_name=user.investment_type or "Medium",
            fund_performance=growth_rate,
            pot_value=new_pot
        )

        db.session.add(statement)
        send_statement_notification(user.email, user.name)


    db.session.commit()
    print(f"Pension statements generated for {len(users)} users.")
