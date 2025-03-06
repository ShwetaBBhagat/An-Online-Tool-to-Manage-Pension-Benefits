import qrcode
import pyotp
import os

def generate_mfa_qr(email, mfa_secret):
    """Generate a QR Code for Google Authenticator setup."""
    otp_uri = f"otpauth://totp/PensionBenefits:{email}?secret={mfa_secret}&issuer=PensionBenefitsApp"

    # Define the directory where QR codes will be saved
    qr_code_dir = os.path.join(os.getcwd(), "backend", "qrcodes")

    # Ensure the directory exists
    if not os.path.exists(qr_code_dir):
        os.makedirs(qr_code_dir)

    # Generate and save QR code
    qr_code_path = os.path.join(qr_code_dir, f"{email}_mfa.png")
    qr = qrcode.make(otp_uri)
    qr.save(qr_code_path)

    print(f"QR Code saved at: {qr_code_path}")  # Debugging log

    return f"/qrcodes/{email}_mfa.png"  # Return the relative path to the saved QR code
