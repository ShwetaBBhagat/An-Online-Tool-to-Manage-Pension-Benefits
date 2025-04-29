from app import app, db
from models.pension_statement_model import PensionStatement
from models.user_model import User
import datetime

# Adjust imports according to your project structure if needed

with app.app_context():
    # 1. Find the user
    user = User.query.filter_by(email='shwetabhagat2012@gmail.com').first()

    if not user:
        print("❌ User not found. Check email.")
    else:
        # 2. Delete existing pension statements for Nov 2024 to March 2025
        start_delete_date = datetime.date(2024, 11, 1)
        end_delete_date = datetime.date(2025, 3, 31)

        existing_statements = PensionStatement.query.filter(
            PensionStatement.user_id == user.id,
            PensionStatement.statement_start_date >= start_delete_date,
            PensionStatement.statement_end_date <= end_delete_date
        ).all()

        for s in existing_statements:
            db.session.delete(s)

        db.session.commit()
        print(f"🗑️ Deleted {len(existing_statements)} existing statements between Nov 2024 - Mar 2025.")

        # 3. Insert 5 new fake pension statements
        statements = [
            {
                "statement_start_date": datetime.date(2024, 11, 1),
                "statement_end_date": datetime.date(2024, 11, 30),
                "statement_date": datetime.date(2024, 12, 1)
            },
            {
                "statement_start_date": datetime.date(2024, 12, 1),
                "statement_end_date": datetime.date(2024, 12, 31),
                "statement_date": datetime.date(2025, 1, 1)
            },
            {
                "statement_start_date": datetime.date(2025, 1, 1),
                "statement_end_date": datetime.date(2025, 1, 31),
                "statement_date": datetime.date(2025, 2, 1)
            },
            {
                "statement_start_date": datetime.date(2025, 2, 1),
                "statement_end_date": datetime.date(2025, 2, 28),
                "statement_date": datetime.date(2025, 3, 1)
            },
            {
                "statement_start_date": datetime.date(2025, 3, 1),
                "statement_end_date": datetime.date(2025, 3, 31),
                "statement_date": datetime.date(2025, 4, 1)
            }
        ]

        for s in statements:
            statement = PensionStatement(
                user_id=user.id,
                account_number="PEN123456789",
                salary=3000.00,
                employer_contribution=300.00,
                employee_contribution=200.00,
                total_contribution=500.00,
                employer_percent=10.0,
                employee_percent=6.66,
                statement_start_date=s["statement_start_date"],
                statement_end_date=s["statement_end_date"],
                statement_date=s["statement_date"],
                fund_name="Standard Life Pension Fund",
                fund_performance=5.2,
                pot_value=12000.00  # can adjust if you want
            )
            db.session.add(statement)

        db.session.commit()
        print("✅ Inserted 5 fresh pension statements successfully!")
