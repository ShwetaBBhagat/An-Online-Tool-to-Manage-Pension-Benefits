from models import db
from datetime import date
from models.user_model import User  # for relationship reference if needed

class PensionStatement(db.Model):
    __tablename__ = 'pension_statements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    statement_start_date = db.Column(db.Date, nullable=False)
    statement_end_date = db.Column(db.Date, nullable=False)
    statement_date = db.Column(db.Date, nullable=False)
    account_number = db.Column(db.String(20))

    salary = db.Column(db.Numeric(10, 2), nullable=False)
    employer_contribution = db.Column(db.Numeric(10, 2), nullable=False)
    employee_contribution = db.Column(db.Numeric(10, 2), nullable=False)
    total_contribution = db.Column(db.Numeric(10, 2), nullable=False)
    employer_percent = db.Column(db.Numeric(5, 2), default=3.00)
    employee_percent = db.Column(db.Numeric(5, 2), default=5.00)

    fund_name = db.Column(db.String(100))
    fund_performance = db.Column(db.Numeric(5, 2))
    pot_value = db.Column(db.Numeric(10, 2))

    user = db.relationship('User', backref=db.backref('statements', lazy=True))

    def __repr__(self):
        return f"<PensionStatement {self.id} for User {self.user_id}>"
