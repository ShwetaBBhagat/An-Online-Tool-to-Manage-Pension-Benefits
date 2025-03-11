from flask_mail import Message, Mail
from threading import Thread
from flask import current_app
import os

mail = Mail()

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)

def send_welcome_email(user_email, user_name, qr_code_path):
    """Send a real-time welcome email with the MFA QR code."""
    msg = Message("Welcome to Pension Benefits App!",
                  sender="your-email@example.com",
                  recipients=[user_email])
    
    msg.body = f"""Hello {user_name},

Welcome to the Pension Benefits Platform! Your account has been successfully created.

To complete your account setup, please enable Multi-Factor Authentication (MFA) using Google Authenticator.

1. Download Google Authenticator from your app store.
2. Scan the attached QR Code in Google Authenticator.
3. Use the generated 6-digit codes during login.

Thank you!
"""

    # Attach QR Code to Email
    with open(qr_code_path, "rb") as qr_code_file:
        msg.attach("mfa_qr_code.png", "image/png", qr_code_file.read())

    # Send email in a separate thread
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
