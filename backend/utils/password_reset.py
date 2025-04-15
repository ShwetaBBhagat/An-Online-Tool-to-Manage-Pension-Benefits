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

def generate_employer_token(email):
    s = URLSafeTimedSerializer(Config.JWT_SECRET_KEY)
    return s.dumps(email, salt="employer-set-password")

def verify_employer_token(token, max_age=3600):
    s = URLSafeTimedSerializer(Config.JWT_SECRET_KEY)
    try:
        email = s.loads(token, salt="employer-set-password", max_age=max_age)
        return email
    except:
        return None