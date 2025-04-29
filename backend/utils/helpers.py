import qrcode
import pyotp
import os
import random
import string
import bcrypt

def generate_mfa_qr(email, mfa_secret):
    """Generate an MFA QR Code for Google Authenticator setup and save it as an image."""
    otp_uri = f"otpauth://totp/PensionBenefits:{email}?secret={mfa_secret}&issuer=PensionBenefitsApp"

    # Define the QR code storage directory
    qr_code_dir = os.path.join(os.getcwd(), "backend", "qrcodes")

    # Ensure the directory exists
    if not os.path.exists(qr_code_dir):
        os.makedirs(qr_code_dir)

    # Generate and save the QR code
    qr_code_path = os.path.join(qr_code_dir, f"{email}_mfa.png")
    qr = qrcode.make(otp_uri)
    qr.save(qr_code_path)

    print(f"QR Code saved at: {qr_code_path}")  # Debugging log

    return qr_code_path  # Return the full path to the saved QR code

def generate_random_password(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8') 
