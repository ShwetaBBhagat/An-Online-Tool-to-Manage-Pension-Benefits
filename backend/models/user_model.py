from models import db
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_roles'), default='user')
    mfa_secret = db.Column(db.String(32), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    ni_number = db.Column(db.String(20), nullable=True)
    current_salary = db.Column(db.Numeric(10, 2), nullable=True)
    employment_status = db.Column(db.Enum('Active', 'Retired'), nullable=True)
    investment_type = db.Column(db.Enum('Low', 'Medium', 'High'), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)
    profile_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.email}>"
