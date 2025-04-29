import jwt
import datetime
from config import Config
from itsdangerous import URLSafeTimedSerializer

def generate_reset_token(email):
    """Generate a secure JWT token for password reset."""
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Token expires in 30 min
    }
    return jwt.encode(payload, Config.JWT_RESET_SECRET, algorithm="HS256")

def verify_reset_token(token):
    """Verify the password reset token."""
    try:
        data = jwt.decode(token, Config.JWT_RESET_SECRET, algorithms=["HS256"])
        return data["email"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

# Generate a token for employer setup
def generate_employer_token(email):
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm="HS256")
    return token

# Verify the employer token when setting password
def verify_employer_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload['email']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None