import jwt
import datetime
from config import Config

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
