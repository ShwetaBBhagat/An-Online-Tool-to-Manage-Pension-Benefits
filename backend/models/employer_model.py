from models import db
from datetime import datetime

class Employer(db.Model):
    __tablename__ = 'employers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(200), nullable=False)  # Allow NULL until setup
    mfa_secret = db.Column(db.String(32), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    users = db.relationship('User', backref='employer', lazy=True)
