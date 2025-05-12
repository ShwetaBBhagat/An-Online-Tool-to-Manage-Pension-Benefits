from models import db
from datetime import datetime

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50))
    percentage = db.Column(db.Numeric(5, 2), default=100.00)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('beneficiaries', lazy=True))

    def __repr__(self):
        return f"<Beneficiary {self.full_name} ({self.percentage}%) for User {self.user_id}>"
